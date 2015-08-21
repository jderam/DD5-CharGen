#!/usr/bin/python3
import uuid
from PC5E import *

clear_screen()

my_PC = PlayerCharacter5E(str(uuid.uuid1()))

my_PC.upd_name("Test Character Guy")

# ABILITY SCORES
my_PC.random_abilities_4d6()
#my_PC.choose_abilities_4d6()

# RACE
my_PC.choose_race()
my_PC.apply_race_ability_bonus()
my_PC.apply_race_attributes()
my_PC.get_race_features()

# BACKGROUND
my_PC.choose_bg()
#my_PC.random_bg()
my_PC.bg_feature()
my_PC.random_bg_tables()
#my_PC.choose_bg_bond()
my_PC.apply_bg_skills()


my_PC.get_trinket()

#print(my_PC.char_id)
#print(my_PC.char_name)
#my_PC.print_ability_scores()
#print("RACE: " + my_PC.char_race_name)
#my_PC.print_bg_data()
#print("Proficiencies: " + str(my_PC.char_skill_profs))
#print("Equipment: " + str(my_PC.char_equip))



# CLASS
my_PC.choose_class()

#print(my_PC.char_class_id)
#print(my_PC.char_class_name)
#print(my_PC.char_hd)
#print(my_PC.char_prime_req)
my_PC.calculate_hp()
my_PC.get_wpn_prof_txt()
my_PC.get_armor_prof_txt()

#print(my_PC.char_wpn_prof_txt)
#print(my_PC.char_armor_prof_txt)

my_PC.print_pc_info()

#clear_screen()

