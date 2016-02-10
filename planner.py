#!/usr/bin/python2.7

from collections import defaultdict
import itertools

GIGETHBASE = """!
  interface GigabitEthernet %s/%s
  no ip address
  switchport
  no shutdown"""

VLANBASE = """!
interface Vlan %s
  ip address 10.0.%s.254/24
%s
  no shutdown"""


class Switch():
    def __init__(self, switch_config):
        self.vlans = self.create_vlans(switch_config)
        #self.cards = self.create_linecards(switch_config)

    def create_vlans(self, switch_config):
        new_vlans = []
        for vlan_conf in switch_config:
            vlan_conf = vlan_conf.items()[0]
            vlan_id, cards = vlan_conf
            new_vlan = Vlan(vlan_id, cards)
            new_vlans.append(new_vlan)

        return new_vlans

class Vlan():
    def __init__(self, id, cards):
        self.id = id
        self.interfaces = self.create_interfaces(cards)
        self.lines = self.create_vlan_lines()

    def create_interfaces(self, cards):
        interfaces = []
        for card in cards:
            card_id = card['card_id']
            start,end = card['id_range']
            id_range = range(start,end)

            if_list = []
            for id in id_range:
                interface = Interface(id, card_id)
                interfaces.append(interface)

        return interfaces

    def create_vlan_lines(self):
        if_lines = self.get_if_vlanlines()
        vlan_line = VLANBASE % (self.id, self.id, if_lines)
        print vlan_line
        return vlan_line
         
    def get_if_vlanlines(self):
        ret_lines = [ iface.vlan_line for iface in self.interfaces ]
        ret_lines = '\n'.join(ret_lines)

        return ret_lines

class Linecard():
    def __init__(self, card_id, id_range):
        self.card_id = card_id
        self.id_range = range(*id_range)

class Interface():
    def __init__(self, id, card_id):
        self.id = id
        self.card_id = card_id
        self.vlan_line = "  untagged GigabitEthernet %s/%s" % (card_id, id)
        self.if_line = GIGETHBASE % (card_id, id)

vlan_plan = [ 
    { 1: [ { 'card_id':1, 'id_range':(0,23) }] },
    { 2: [ { 'card_id':1, 'id_range':(24,47) }] },
    { 3: [ { 'card_id':1, 'id_range':(48,71) }] },
    { 4: [ { 'card_id':1, 'id_range':(24,47) },
                     { 'card_id':2, 'id_range':(0,5) }] },
    { 5: [ { 'card_id':2, 'id_range':(6,29) } ] },
    { 6: [ { 'card_id':2, 'id_range':(30,53) } ] },
    { 7: [ { 'card_id':2, 'id_range':(54,77) } ] },
    { 8: [ { 'card_id':2, 'id_range':(78,89) },
           { 'card_id':3, 'id_range':(0,11) } ] },
    { 9: [ { 'card_id':3, 'id_range':(12,35) } ] },
    { 10: [ { 'card_id':3, 'id_range':(36,59) } ] },
    { 11: [ { 'card_id':3, 'id_range':(60,83) } ] },
    { 12: [ { 'card_id':3, 'id_range':(84,89) },
                      { 'card_id':4, 'id_range':(0,17) }] },
    ]

switch = Switch(vlan_plan)
vlans = switch.vlans


tmp_if = [ vlan.interfaces for vlan in vlans ]
interfaces = itertools.chain(*tmp_if)

for i in interfaces:
    print i.if_line

for i in vlans:
    print vlan.lines
