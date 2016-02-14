#!/usr/bin/python2.7

from collections import defaultdict
import itertools
import numpy as np

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

LINECARDLOC = "/opt/lan_e1000/LAN_e1000/configs/linecards.defs"

class Lan(object):
    def __init__(self, col_count=12, col_size=24):
        self.switch = Switch(vlan_plan)
        self.columns = self.create_columns(col_count, col_size)
        print super(Lan,self)

    #def __setitem__(self, key, value):
    #    print self.columns

    def create_columns(self, col_count, col_size):
        col_range = range(1,col_count+1)
        ret_cols = [ Column(id, col_size) for id in col_range ]

        return ret_cols
        
class Column(Lan):
    def __init__(self, id, size):
#        self.people = create_people(size)
        print dir(super(Column, self).__init__())
        self.vlan = id

class Switch():
    def __init__(self, switch_config):
        self.vlans = self.create_vlans(switch_config)
        self.cards = self.create_linecards(LINECARDLOC)

    def create_vlans(self, switch_config):
        new_vlans = []
        for vlan_conf in switch_config:
            vlan_conf = vlan_conf.items()[0]
            vlan_id, cards = vlan_conf
            new_vlan = Vlan(vlan_id, cards)
            new_vlans.append(new_vlan)

        return new_vlans

    def create_linecards(self, conf_loc):
        conf_lines = '\n'.join(open(conf_loc,'r').readlines())
        exec(conf_lines) # linecards = { ........ }
        for cardtype in linecards:
            name,slots,size = cardtype.values()
            cards = [ Linecard(name,slot,size) for slot in slots ]

        linecards = itertools.chain(*cards)

        return linecards

class Vlan():
    def __init__(self, id, cards):
        self.id = id
        self.lines = self.create_vlan_lines()

    def create_vlan_lines(self):
        if_lines = self.get_if_vlanlines()
        vlan_line = VLANBASE % (self.id, self.id, if_lines)

        return vlan_line
         
    def get_if_vlanlines(self):
        #ret_lines = [ iface.vlan_line for iface in self.interfaces ]
        #ret_lines = '\n'.join(ret_lines)
        ret_lines = ''

        return ret_lines

class Linecard():
    def __init__(self, name, slot, size):
        self.name = name
        self.slot = slot
        self.size = size

        self.interfaces = self.create_interfaces(self.size)

    def create_interfaces(self, size):
        interfaces = []
        id_range = range(0,size)

        if_list = []
        for id in id_range:
            interface = Interface(id)
            interfaces.append(interface)

        return interfaces

class Interface():
    def __init__(self, id):
        self.id = id
        self.vlan_line = "  untagged GigabitEthernet %s" % (id)
        self.if_line = GIGETHBASE % (1, id)

lan = Lan()
#vlans = switch.vlans
