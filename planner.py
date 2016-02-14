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

LINECARDLOC = "/opt/lan_e1000/LAN_e1000/configs/linecards.defs"

class Lan():
    def __init__(self, column_no=12, column_size=24):
        self.switch = Switch()
        self.columns = self.create_columns(column_no, column_size)
        self.vlans = self.create_vlans()
        
    def create_columns(self, col_count, col_size):
        col_range = range(1,col_count+1)
        ret = [ self.new_col(id, col_size, self.switch) for id in col_range ]

        return ret

    def new_col(self, id, col_size, switch):
        return Column(id, col_size, switch)

    def create_vlans(self):
        vlans = []
        for col in self.columns:
            new_vlan = Vlan(col.id)
            for vlan_if in range(0, col.size):
                vlan_if = self.switch.open_ifs.pop(0)
                new_vlan.add_interface(vlan_if)

            vlans.append(new_vlan)

        return vlans
         
class Column():
    def __init__(self, id, size, switch=None):
        self.id = id
        self.switch = switch
        self.size = size

        #self.switchports = self.switch.create_vlans(self.size)

class Switch():
    def __init__(self):
        self.cards = self.create_linecards(LINECARDLOC)
        self.open_ifs = self.get_open_ifs()

    def create_linecards(self, conf_loc):
        conf_lines = '\n'.join(open(conf_loc,'r').readlines())
        exec(conf_lines) # linecards = { ........ }
        for cardtype in linecards:
            name  = cardtype['name']
            slots  = cardtype['slots']
            size  = cardtype['size']
            cards = [ Linecard(name,slot,size) for slot in slots ]

        linecards = itertools.chain(cards)
        return linecards

    def get_open_ifs(self):
        open_ifs = []
        for card in self.cards:
            for card_if in card.interfaces:
                if not card_if.vlan_id:
                    open_ifs.append(card_if)

        return open_ifs

class Vlan():
    def __init__(self, id):
        self.id = id
        self.interfaces = []
        self.lines = self.create_vlan_lines()

    def add_interface(self, interface):
        self.interfaces.append(interface)

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
        self.interfaces = self.create_interfaces()

    def create_interfaces(self):
        interfaces = []
        for id in range(0, self.size):
            interfaces.append(self.new_interface(id))

        return interfaces

    def new_interface(self, id):
         return Interface(id, self)

class Interface():
    def __init__(self, id, card):
        self.id = id
        self.card = card
        self.vlan_id = None

        #self.vlan_line = "  untagged GigabitEthernet %s" % (id)
        #self.if_line = GIGETHBASE % (1, id)

lan = Lan(12, 24)
