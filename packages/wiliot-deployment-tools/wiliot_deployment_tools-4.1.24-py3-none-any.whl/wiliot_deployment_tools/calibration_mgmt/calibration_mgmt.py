import datetime
import sys
import time
from wiliot_deployment_tools.api.extended_api import EXCEPTIONS_TO_CATCH, BridgeThroughGatewayAction, ExtendedEdgeClient, GatewayType
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.common.utils_defines import  SEC_TO_SEND, BROADCAST_DST_MAC


class CalibrationManagementError(Exception):
    pass
  

class CalibrationManagementClient(ExtendedEdgeClient):
    
    is_first_call = True

    def get_relevant_bridges(self, gateway_id):
        """
        Returns seen bridges by gateway that are associated to owner and have ble version with calibration management support
        :type gateway_id: str
        :param gateway_id: gateway ID
        :rtype: list
        :return: list of relevant bridge IDs
        """
        bridges = self.get_seen_bridges(gateway_id)
        relevant_bridges = bridges
        not_owned_brgs = []
        not_support_version = []
        for bridge in bridges:
            try:
                brg_ble = self.get_brg_ble_version(bridge)
            except Exception as e:
                if "not owned" in str(e):
                    not_owned_brgs.append(bridge)
                    relevant_bridges.remove(bridge)
                    continue
            if not self.check_ble_calibration_mgmt_support(brg_ble):
                not_support_version.append(bridge)
                relevant_bridges.remove(bridge)
        if self.is_first_call:
            # print warning once
            self.is_first_call = False
            debug_print(f"Warning! bridges id:{not_owned_brgs} are not owned, skiping bridges")
            debug_print(f'Bridges {not_support_version} do not support calibration management!')
        return relevant_bridges


    @staticmethod
    def check_ble_calibration_mgmt_support(ble_ver):
        """
        checks if calibration management is supported for BLE version
        :rtype: bool
        :return: True if supported, False otherwise
        """
        ble_ver = ble_ver.split('.')
        if not ((int(ble_ver[0]) > 3) or
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 14) or \
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 13 and int(ble_ver[2]) > 61)):
            return False
        else:
            return True


    def send_calib_mgmt_pkt(self, bridge_id, payload, gateway_id=None,
                          silent=False, seconds_to_send=1):
        """
        send calibration management packet to bridge
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to send to bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type silent: bool
        :param silent: print calibration management packet parameters
        :type seconds_to_send: int
        :param seconds_to_send: seconds to repeat packet
        :rtype: bool
        :return: True if sent, False otherwise
        """
        via_gw = []
        if gateway_id is None:
            via_gw = self.get_bridge_relevant_gw(bridge_id, get_gw_list=True)
        else:
            via_gw.append(gateway_id)
        seconds_to_send = datetime.timedelta(seconds=seconds_to_send)
        for gw in via_gw:
            # Check BRG Compatability
            gw_type = self.get_gateway_type(gw)
            if gw_type == GatewayType.WIFI:
                rxtx = datetime.timedelta(milliseconds=
                                    self.get_gateway(gw)['reportedConf']['additional']['rxTxPeriodMs'])
            if gw_type == GatewayType.MOBILE:
                rxtx = datetime.timedelta(milliseconds=140)
            reps = seconds_to_send // rxtx + 1
            if not silent:
                debug_print(f'Sending packet through GW {gw} for {seconds_to_send.total_seconds()} seconds, rxTx = {int(rxtx.total_seconds()*1000)} ms, reps = {reps}')
            try:
                res = self.send_bridge_action_through_gw(gw,
                                                        BridgeThroughGatewayAction.SPARSE_37,
                                                        payload, bridge_id, reps=reps)
            except EXCEPTIONS_TO_CATCH as e:
                debug_print('Exception caught when sending calibration management packet!')
                debug_print(e)
                return False
        return res
    
    def check_calib_mgmt_received(self, gateway_id, bridge_id, payload, time_sent):
        """
        check if calibration management packet was received by bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to check
        :type time_sent: datetime
        :param time_sent: time packet was sent
        :rtype bool
        :return: True if packet was received, None otherwise
        """
        hours_back = (datetime.datetime.now() - time_sent + datetime.timedelta(seconds=5)).total_seconds() / 3600
        acks = self.get_acks(gateway_id, hours_back)
        if acks is None:
            return None
        acks = acks[(acks['actionType'] == BridgeThroughGatewayAction.SPARSE_37) &
                    (acks['bridgeId'] == bridge_id) &
                    (acks['payload'].apply(lambda x: x[1])
                     == payload[1])] 
        if len(acks) > 0:
            return acks.to_dict()
        return None

        
    def send_calibration_packet_until_ack(self, gateway_id, bridge_id, minutes_timeout=3, mode=0):
        """
        send calibration management packet repeatedly until it is received by the bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to send
        :type minutes_timeout: int
        :param minutes_timeout: timeout
        :rtype: dict
        :return: dict of {bridgeID: ack status (bool)} pairs
        """
        brg_version = self.get_brg_ble_version(bridge_id)
        if not self.check_ble_calibration_mgmt_support(brg_version):
            debug_print(f"Error! bridge:{bridge_id} ble version does'nt support calibration mgmt")
            return False
        time_sent = datetime.datetime.now()
        payload = '0{:01d}{:019d}'.format(mode, 0)
        debug_print(f'Configuring {bridge_id} To Calibration mode {mode} | Max Waiting time {minutes_timeout} minutes')
        self.send_calib_mgmt_pkt(bridge_id, payload, gateway_id, silent=False, seconds_to_send=SEC_TO_SEND)
        time_gw_stops = time_sent + datetime.timedelta(seconds=SEC_TO_SEND)
        time_end = time_sent + datetime.timedelta(minutes=minutes_timeout)
        curr_time = time_sent
        ack = None
        print('Waiting For Ack...', end='', flush=True)
        while curr_time < time_end and ack is None:
            curr_time = datetime.datetime.now()
            if curr_time > time_gw_stops - datetime.timedelta(seconds=1):  # 1 second buffer
                self.send_calib_mgmt_pkt(bridge_id, payload, gateway_id, silent=True, seconds_to_send=SEC_TO_SEND)
                time_gw_stops = datetime.datetime.now() + datetime.timedelta(seconds=SEC_TO_SEND)
                print('!', end='')
                sys.stdout.flush()
            time.sleep(0.5)
            print('.', end='')
            sys.stdout.flush()
            if gateway_id is None:
                gws = self.get_bridge_relevant_gw(bridge_id, get_gw_list=True)
                for gw in gws:
                    ack = self.check_calib_mgmt_received(gw, bridge_id, payload, time_sent)
                    if ack:
                        break
            else:
                ack = self.check_calib_mgmt_received(gateway_id, bridge_id, payload, time_sent)
        print()  # enter newline
        ack_received = False
        if ack is not None:
            ack_received = True
            debug_print(f'Ack Received after {datetime.datetime.now() - time_sent}')
        else:
            debug_print(f'Ack not received after {datetime.datetime.now() - time_sent}!')
        return {bridge_id: ack_received}
    

    def broadcast_calib_mgmt_packet(self, payload, gateway_id, silent=False, seconds_to_send=1):
        """
        broadcast packet to all bridges connected to GW
        :type packet: PowerManagementPacket
        :param packet: packet to broadcast
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type silent: bool
        :param silent: print power management packet parameters
        :rtype: tuple
        :return: results (bool), bridges sent to (list)
        """
        if not self.check_gw_compatible_for_action(gateway_id):
            raise CalibrationManagementError(f'Gateway {gateway_id} not compatible with power management! '
                                       f'Try to update GW version') 
        brgs_to_broadcast = self.get_relevant_bridges(gateway_id)
        for bridge in brgs_to_broadcast:
            try:
                bridge_ver = self.get_brg_ble_version(bridge)
            except Exception as e:
                if "not owned" in str(e):
                    brgs_to_broadcast.remove(bridge)
                    continue
            bridge_ver = self.get_brg_ble_version(bridge)
            if not self.check_ble_calibration_mgmt_support(bridge_ver):
                brgs_to_broadcast.remove(bridge)
        if not silent:
            debug_print(f'Broadcasting Packet to bridges {brgs_to_broadcast}')
        res = self.send_calib_mgmt_pkt(BROADCAST_DST_MAC, payload, gateway_id, silent, seconds_to_send)
        return res, brgs_to_broadcast


    def check_calib_mgmt_broadcast_received(self, gateway_id, bridges, payload, time_sent):
        """
        check if power management broadcast was received by bridges
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type bridges: list
        :param bridges: list of Bridge IDs
        :type time_sent: datetime
        :param time_sent: time packet was sent
        :rtype: dict
        :return: dict of bridgeIDs:received status
        """
        hours_back = (datetime.datetime.now() - time_sent + datetime.timedelta(seconds=10)).total_seconds() / 3600
        acks = self.get_acks(gateway_id, hours_back)
        result = dict().fromkeys(bridges)
        for brg in bridges:
            if acks is None:
                result[brg] = False
                continue
            brg_acks = acks[(acks['actionType'] == BridgeThroughGatewayAction.SPARSE_37) &
                    (acks['bridgeId'] == brg) &
                    (acks['payload'].apply(lambda x: x[1])
                     == payload[1])] 
            if len(brg_acks) > 0:
                result[brg] = True
            else:
                result[brg] = False
        return result


    def broadcast_calibration_packet_until_ack(self, gateway_id,minutes_timeout=3, mode=0):
        """
        send power management packet repeatedly until it is received by the all 'seen' bridges
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type packet: PowerManagementPacket
        :param packet: packet to send
        :type minutes_timeout: int
        :param minutes_timeout: timeout
        :rtype: dict
        :return: dict of {bridgeID: ack status (bool)} pairs
        """
        time_sent = datetime.datetime.now()
        payload = '0{:01d}{:019d}'.format(mode, 0)
        res, bridges = self.broadcast_calib_mgmt_packet(payload, gateway_id, silent=False, seconds_to_send=SEC_TO_SEND)
        debug_print(f'Configuring {bridges} To calibration mode {mode} | Max Waiting time {minutes_timeout} minutes')
        time_gw_stops = time_sent + datetime.timedelta(seconds=SEC_TO_SEND)
        time_end = time_sent + datetime.timedelta(minutes=minutes_timeout)
        curr_time = time_sent
        ack = self.check_calib_mgmt_broadcast_received(gateway_id, bridges, payload, time_sent)
        print('Waiting For Ack...', end='', flush=True)
        while curr_time < time_end and not all(ack.values()):
            curr_time = datetime.datetime.now()
            if curr_time > (time_gw_stops - datetime.timedelta(seconds=1)):  # 1 second buffer
                new_bridges = self.get_relevant_bridges(gateway_id)
                if bridges != new_bridges:
                    bridges = new_bridges
                    debug_print(f'Bridges seen by GW changed while broadcasting! now broadcasting to {bridges}')
                self.broadcast_calib_mgmt_packet(payload, gateway_id, silent=True, seconds_to_send=SEC_TO_SEND)
                time_gw_stops = datetime.datetime.now() + datetime.timedelta(seconds=SEC_TO_SEND)
                print('!', end='')
                sys.stdout.flush()
            time.sleep(0.5)
            print('.', end='')
            sys.stdout.flush()
            ack = self.check_calib_mgmt_broadcast_received(gateway_id, bridges, payload, time_sent)
        print()  # enter newline
        if not all(ack.values()):
            # list of bridges which did not return ack
            brgs_missed = list(dict(filter(lambda x: x[1] is False, ack.items())).keys())
            debug_print(f'Packet not received by bridges {brgs_missed} after {minutes_timeout} minutes!')
        else:
            debug_print(
                f'Ack Received after {datetime.datetime.now() - time_sent} by bridges {list(ack.keys())}')
        return ack