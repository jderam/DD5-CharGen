#!/usr/bin/python3
import uuid
from PC5E import *

clear_screen()

myPC = PlayerCharacter5E(str(uuid.uuid1()))

myPC.upd_name("Test Character Guy")

# ABILITY SCORES
myPC.random_abilities_4d6()
#myPC.choose_abilities_4d6()

# RACE
myPC.choose_race()
myPC.apply_race_ability_bonus()
myPC.apply_race_attributes()
myPC.get_race_features()

# BACKGROUND
myPC.choose_bg()
#myPC.random_bg()
myPC.bg_feature()
myPC.random_bg_tables()
#myPC.choose_bg_bond()
myPC.apply_bg_skills()


myPC.get_trinket()

#print(myPC.char_id)
#print(myPC.char_name)
#myPC.print_ability_scores()
#print("RACE: " + myPC.char_race_name)
#myPC.print_bg_data()
#print("Proficiencies: " + str(myPC.char_skill_profs))
#print("Equipment: " + str(myPC.char_equip))



# CLASS
myPC.choose_class()

#print(myPC.char_class_id)
#print(myPC.char_class_name)
#print(myPC.char_hd)
#print(myPC.char_prime_req)
myPC.calculate_hp()
myPC.get_wpn_prof_txt()
myPC.get_armor_prof_txt()

#print(myPC.char_wpn_prof_txt)
#print(myPC.char_armor_prof_txt)

myPC.lang_prof()
myPC.tool_prof()

myPC.print_pc_info()

#clear_screen()

