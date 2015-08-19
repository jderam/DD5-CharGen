#!/usr/bin/python3
import uuid
import PC5E

my_PC = PC5E.PlayerCharacter5E(str(uuid.uuid1()))

my_PC.upd_name("Test Character Guy")


my_PC.random_abilities_4d6()
#my_PC.choose_abilities_4d6()

my_PC.choose_race()
my_PC.apply_race_ability_bonus()

#my_PC.choose_bg()
my_PC.random_bg()
my_PC.bg_feature()
my_PC.random_bg_tables()
#my_PC.choose_bg_bond()



my_PC.apply_bg_skills()


my_PC.get_trinket()

print(my_PC.char_id)
print(my_PC.char_name)
my_PC.print_ability_scores()
print("RACE: " + my_PC.char_race_name)
my_PC.print_bg_data()
print("Proficiencies: " + str(my_PC.char_skill_profs))
print("Equipment: " + str(my_PC.char_equip))

my_PC.get_race_features()


#clear_screen()

