#!/usr/bin/python3

from __future__ import print_function

import random
import os
import sqlite3
conn = sqlite3.connect('dnd5.db')
c = conn.cursor()

def clear_screen():
    """ function to clean the screen """
    osname = os.name
    if osname == "posix":
        os.system('clear')
    elif osname == "nt" or osname == "dos":
        os.system('cls')
    else:
        for i in xrange(100):
            print("")

def print_menu(user_list):
    for i in xrange(1,len(user_list)+1):
        print(str(i) + " " + user_list[i-1])


def roll_dice(qty, num_sides):
    total = 0
    for i in range(qty):
        total += random.randint(1,num_sides)
    return total

def roll_4d6():
    rolls = [random.randint(1,6), random.randint(1,6), random.randint(1,6), random.randint(1,6)]
    rolls.sort()
    return (rolls[1] + rolls[2] + rolls[3])


def pad_ability_score(score):
    if score < 10:
        return " " + str(score)
    else:
        return str(score)

def pad_modifier(modifier):
    if modifier < 0:
        return str(modifier)
    else:
        return "+" + str(modifier)

ability_modifiers = { 1: -5,
                      2: -4,
                      3: -4,
                      4: -3,
                      5: -3,
                      6: -2,
                      7: -2,
                      8: -1,
                      9: -1,
                      10: 0,
                      11: 0,
                      12: 1,
                      13: 1,
                      14: 2,
                      15: 2,
                      16: 3,
                      17: 3,
                      18: 4,
                      19: 4,
                      20: 5,
                      21: 5,
                      22: 6,
                      23: 6,
                      24: 7,
                      25: 7,
                      26: 8,
                      27: 8,
                      28: 9,
                      29: 9,
                      30: 10}

class PlayerCharacter5E(object):
    """D&D 5E Player Character"""


    def __init__(self, char_id):
        self.char_id = char_id
        self.char_name = None
        self.char_lvl = 1
        self.char_alignment = ""
        self.char_prof_bonus = 2
        self.char_ability_scores = {"STR":0, "DEX":0, "CON":0, "INT":0, "WIS":0, "CHA":0}
        self.char_race_id = 0
        self.char_race_name = ""
        self.char_race_features = []
        self.char_size = ""
        self.char_speed = 0
        self.char_darkvision = 0
        self.char_bg_id = 0
        self.char_bg_name = None
        self.char_class_id = 0
        self.char_class_name = None
        self.char_skills = {"Acrobatics":0,
                       "Animal Handling":0,
                       "Arcana":0,
                       "Athletics":0,
                       "Deception":0,
                       "History":0,
                       "Insight":0,
                       "Intimidation":0,
                       "Investigation":0,
                       "Medicine":0,
                       "Nature":0,
                       "Perception":0,
                       "Performance":0,
                       "Persuasion":0,
                       "Religion":0,
                       "Sleight of Hand":0,
                       "Stealth":0,
                       "Survival":0}
        self.char_skill_profs = []
        self.char_tool_profs = []
        self.char_languages = []
        self.char_weapons = []
        self.char_armor = []
        self.char_equip = []
        self.char_gp = 0.0
    
    def __repr__(self):
        """ define the representation of a character, which will be a list of data points """
        return [self.char_id, self.char_name, self.char_lvl, self.char_race_name, self.char_class_name, self.char_bg_name, self.char_ability_scores]
    
    # EASY STUFF LIKE NAME, ALIGNMENT, ETC.
    
    def upd_name(self, char_name):
        self.char_name = char_name
    
    def choose_align(self):
        """ allow user to choose alignment """
        alignments = {1: "Lawful Good",
                      2: "Neutral Good",
                      3: "Chaotic Good",
                      4: "Lawful Neutral",
                      5: "Neutral",
                      6: "Chaotic Neutral",
                      7: "Lawful Evil",
                      8: "Neutral Evil",
                      9: "Chaotic Evil"}
        for i in range(1,10):
            print(i + " " + alignments[i])
        align_id = int(raw_input("Enter the number of the alignment you'd like: "))
        self.char_alignment = alignments[align_id]
    

    # ABILITY SCORES
    
    def choose_abilities_4d6(self):
        abilities = { 1:"STR", 2:"DEX", 3:"CON", 4:"INT", 5:"WIS", 6:"CHA" }
        scores = []
        for i in range(6):
            scores.append(roll_4d6())
        scores.sort()
        print("here are your scores: " + str(scores))
        while len(scores) > 0:
            curr_score = scores.pop()
            if len(scores) == 5:
                print("your highest score is " + str(curr_score))
            else:
                print("your next highest score is " + str(curr_score))
            print(abilities)
            response = input("Enter the number of the ability you'd like to assign this score to: ")
            #while (abilities.has_key(int(response)) == False):
            while (int(response) in abilities) == False:
                response = input("Invalid entry. Please try again: ")
            self.char_ability_scores[abilities[int(response)]] = curr_score
            del abilities[int(response)]
            print("")
        print("")
        #print "Here are your final scores: ", self.char_ability_scores
    
    def random_abilities_4d6(self):
        for ab in self.char_ability_scores.keys():
            self.char_ability_scores[ab] = (roll_4d6())
        #print "Here are your final scores: ", self.char_ability_scores



    
    # RACE

    def choose_race(self):
        """ allow the user to select a race """
        c.execute("SELECT race_id, race_name, bonus_text FROM races")
        race_list = c.fetchall()
        c.execute("SELECT Max(Length(race_name)) FROM races")
        longest_race_name = c.fetchone()[0]
        print("Choose a race:")
        print()
        for race in race_list:
            race_id = race[0]
            race_name = race[1]
            race_bonus_text = race[2]
            #print(str(race_id) + ". " + race_name + ": " + race_bonus_text)
            print("{0:>2}. {1:<{2}} {3}".format(race_id, race_name, longest_race_name, race_bonus_text))
        self.char_race_id = int(input("Enter the number of the race you'd like: "))
        c.execute("SELECT race_name FROM races WHERE race_id=?", (self.char_race_id,))
        self.char_race_name = c.fetchone()[0]
        #print "You've chosen", self.char_race_name
        clear_screen()
    
    def random_race(self):
        """ randomly select a race """
        # TODO: weight the selection based on ability scores and potential bonuses
        
    
    def apply_race_ability_bonus(self):
        """ apply racial ability bonuses """
        # the way I'm handling "ANY" bonuses is not very efficient. need to revisit.
        c.execute("SELECT ability, bonus FROM race_ability_bonuses WHERE race_id=?",(self.char_race_id,))
        bonus_list = c.fetchall()
        ability_menu = ["STR","DEX","CON","INT","WIS","CHA"]
        # process all the normal bonuses
        for row in bonus_list:
            ability = str(row[0])
            bonus = int(row[1])
            if ability != "ANY":
                self.char_ability_scores[ability] += bonus
                ability_menu.remove(ability)
        # process the "ANY" bonuses
        for row in bonus_list:
            ability = str(row[0])
            bonus = int(row[1])
            if ability == "ANY":
                ability_menu_dict = {}
                ability_menu_num = 1
                for ab in ability_menu:
                    ability_menu_dict[ability_menu_num] = ab
                    ability_menu_num += 1
                for item in ability_menu_dict.items():
                    print(str(item[0]) + " " + item[1])
                    #print(item)
                ability_num = int(input("Enter the number of the ability you'd like to apply your +" + str(bonus) + " bonus to: "))
                ability = ability_menu_dict[ability_num]
                self.char_ability_scores[ability] += bonus
                ability_menu.remove(ability)
        clear_screen()

    def apply_race_attributes(self):
        c.execute("SELECT size FROM races WHERE race_id=?",(self.char_race_id,))
        self.char_size = str(c.fetchone()[0])
        c.execute("SELECT speed FROM races WHERE race_id=?",(self.char_race_id,))
        self.char_speed = int(c.fetchone()[0])
        c.execute("SELECT darkvision FROM races WHERE race_id=?",(self.char_race_id,))
        self.char_darkvision = int(c.fetchone()[0])
    
    def get_race_features(self):
        c.execute("SELECT feature_name, feature_text FROM race_features WHERE race_id=?",(self.char_race_id,))
        self.char_race_features = c.fetchall()
        # results is a list of tuples, i.e. (feature_name, feature_desc)
        #print(results)
    
    # SPECIAL RACE SUBROUTINES
    
    def random_dragonborn_ancestry(self):
        """" randomly select dragon type for breath weapon type and damage resistance """
        self.char_da_id = roll_dice(1,10)
        c.execute("SELECT dragon_color, damage_type, breath_weapon, breath_weapon_save FROM draconic_ancestry WHERE da_id=?",(self.char_da_id,))
        results = c.fetchone()[0]
        self.char_da_dragon_color = str(results[0])
        self.char_da_damage_type = str(results[1])
        self.char_da_breath_weapon = str(results[2])
        self.char_da_breath_weapon_save = str(results[3])
    
    def choose_dragonborn_ancestry(self):
        """ probably never gonna add this. fuck dragonborns. """
    
    # BACKGROUND
    
    def choose_bg(self):
        """ present user with a list of backgrounds so they can choose one """
        c.execute("SELECT bg_id, background FROM bg_backgrounds")
        bg_list = c.fetchall()
        print("Choose a background:")
        print()
        for bg in bg_list:
            #print(bg[0] + " " + str(bg[1]))
            print("{0:>2}. {1}".format(bg[0], bg[1]))
        print()
        self.char_bg_id = int(input("Enter the number of the background you'd like: "))
        c.execute("SELECT background FROM bg_backgrounds WHERE bg_id=?", (self.char_bg_id,))
        self.char_bg_name = str(c.fetchone()[0])
        #print "You've chosen", self.char_bg_name
        clear_screen()

    def random_bg(self):
        """ randomly select a background """
        # TODO: Add support for different source options
        c.execute("SELECT bg_id, background, source FROM bg_backgrounds")
        self.bg_list = c.fetchall()
        self.char_bg_id = roll_dice(1,len(self.bg_list)) #this will only work for Basic+PHB content
        self.char_bg_name = str(self.bg_list[self.char_bg_id-1][1])
        
    def bg_feature(self):
        """ get the feature for the character's background """
        c.execute("SELECT feature_name FROM bg_features WHERE bg_id=?", (self.char_bg_id,))
        self.char_bg_feature = str(c.fetchone()[0])

    def random_bg_tables(self):
        """ randomly roll on all the bg tables: personality trait, bond, ideal, flaw """
        # check for specialty
        c.execute("SELECT Count(1) FROM bg_spec_titles WHERE bg_id=?", (self.char_bg_id,))
        if int(c.fetchone()[0]) > 0:
            c.execute("SELECT spec_title, range FROM bg_spec_titles WHERE bg_id=?", (self.char_bg_id,))
            spec_data = c.fetchone()
            self.bg_spec_title = str(spec_data[0])
            self.bg_spec_range = int(spec_data[1])
            spec_roll = roll_dice(1,self.bg_spec_range)
            c.execute("SELECT spec_desc FROM bg_specialty WHERE bg_id=? AND spec_id=?", (self.char_bg_id,spec_roll))
            self.char_bg_specialty = str(c.fetchone()[0])
            #print self.bg_spec_title.upper() + ": " + self.char_bg_specialty
        else:
            self.char_bg_specialty = None
        
        self.ptrait_id = roll_dice(1,8)
        self.ideal_id = roll_dice(1,6)
        self.bond_id = roll_dice(1,6)
        self.flaw_id = roll_dice(1,6)
        # trait
        c.execute("SELECT trait_desc FROM bg_traits WHERE bg_id=? AND trait_id=?", (self.char_bg_id,self.ptrait_id))
        self.char_ptrait = str(c.fetchone()[0])
        # ideal
        c.execute("SELECT ideal_desc FROM bg_ideals WHERE bg_id=? AND ideal_id=?", (self.char_bg_id,self.ideal_id))
        self.char_ideal = str(c.fetchone()[0])
        # bond
        c.execute("SELECT bond_desc FROM bg_bonds WHERE bg_id=? AND bond_id=?", (self.char_bg_id,self.bond_id))
        self.char_bond = str(c.fetchone()[0])
        # flaw
        c.execute("SELECT flaw_desc FROM bg_flaws WHERE bg_id=? AND flaw_id=?", (self.char_bg_id,self.flaw_id))
        self.char_flaw = str(c.fetchone()[0])


    def choose_bg_trait(self):
        """  """
    
    def choose_bg_ideal(self):
        """  """


    def choose_bg_bond(self):
        """ present user with a list of bonds so they can choose one """
        c.execute("SELECT bond_id, bond_desc FROM bg_bonds WHERE bg_id=?", (self.char_bg_id,))
        bond_list = c.fetchall()
        for bond in bond_list:
            print(bond[0] + " " + bond[1])
        self.char_bg_bond_id = int(input("Enter the number of the bond you'd like: "))
        c.execute("SELECT bond_desc FROM bg_bonds WHERE bg_id=? AND bond_id=?", (self.char_bg_id, self.char_bg_bond_id))
        self.char_bg_bond = str(c.fetchone()[0])
        print("BOND: " + self.char_bg_bond)
    
    def choose_bg_flaw(self):
        """  """
    
    

    def print_bg_data(self):
        """ print background info to screen """
        print("BACKGROUND: " + self.char_bg_name)
        if self.char_bg_specialty != None:
            print(self.bg_spec_title.upper() + ": " + self.char_bg_specialty)
        print("PERSONALITY TRAIT: " + self.char_ptrait)
        print("IDEAL: " + self.char_ideal)
        print("BOND: " + self.char_bond)
        print("FLAW: " + self.char_flaw)

    def apply_bg_skills(self):
        """ add skills from background to the character's skill proficiency list """
        c.execute("SELECT s.skill_name FROM skills s JOIN bg_skills bs ON s.skill_id = bs.skill_id WHERE bs.bg_id=?", (self.char_bg_id,))
        self.bg_skills = c.fetchall()
        for skill in self.bg_skills:
            self.char_skill_profs.append(str(skill[0]))

    def apply_bg_tools(self):
        """  """
    
    def apply_bg_lang(self):
        """ not used. a single languages function integrating race and background languages is used later """
    
    def apply_bg_equip(self):
        """  """
    
    # CLASS
    
    def choose_class(self):
        """ allow the user to select a class """
        c.execute("SELECT class_id, class_name, hd, prime_req FROM classes")
        class_list = c.fetchall()
        # returns list of tuples
        c.execute("SELECT Max(Length(class_name)) FROM classes")
        longest_class_name = c.fetchone()[0]
        print("Choose a class:")
        print()
        for pc_class in class_list:
            class_id = pc_class[0]
            class_name = pc_class[1]
            hd = pc_class[2]
            prime_req = pc_class[3]
            #print(str(race_pk) + ". " + race_name + ": " + race_bonus_text)
            print("{0:>2}. {1:<{2}} HD: d{3:<2} ".format(class_id, class_name, longest_class_name, str(hd)))
        self.char_class_id = int(input("Enter the number of the class you'd like: "))
        c.execute("SELECT class_name, hd, prime_req FROM classes WHERE class_id=?", (self.char_class_id,))
        class_data = c.fetchone()
        self.char_class_name = class_data[0]
        self.char_hd = class_data[1]
        self.char_prime_req = class_data[2]
        #print "You've chosen", self.char_race_name
        clear_screen()
    
    def random_class(self):
        """ randomly select a class """
        
    def calculate_hp(self):
        self.char_hp = self.char_hd + ability_modifiers[self.char_ability_scores["CON"]]
        if self.char_lvl > 1:
            self.char_hp += roll_dice(self.char_lvl - 1, self.char_hd) + ((self.char_lvl - 1) * ability_modifiers[self.char_ability_scores["CON"]])

    def get_wpn_prof_txt(self):
        """ """
        c.execute("SELECT wpn_prof_text FROM class_wpn_prof WHERE class_id=? AND wpn_prof_text IS NOT NULL",(self.char_class_id,))
        self.char_wpn_prof_txt = c.fetchone()[0]
    
    def get_wpn_prof_ids(self):
        """ """
    
    def get_armor_prof_txt(self):
        """ """
        c.execute("SELECT armor_prof_text FROM class_armor_prof WHERE class_id=? AND armor_prof_text IS NOT NULL",(self.char_class_id,))
        self.char_armor_prof_txt = c.fetchone()[0]
    
    def get_armor_prof_ids(self):
        """ """
    
    
    
    
    # OTHER

    def lang_prof(self):
        if self.char_race_id > 0 and self.char_bg_id > 0:
            c.execute("SELECT lang_id FROM race_lang WHERE race_id=?",(self.char_race_id,))
            race_lang_ids = c.fetchall() #list of tuples
            c.execute("SELECT lang_id FROM bg_lang WHERE bg_id=?",(self.char_bg_id,))
            bg_lang_ids = c.fetchall() #list of tuples
            all_lang_ids = race_lang_ids + bg_lang_ids
            specific_lang_ids = []
            choice_lang_ids = []
            for lang_id in all_lang_ids:
                if lang_id[0] == 0:
                    choice_lang_ids.append(lang_id[0])
                else:
                    specific_lang_ids.append(lang_id[0]) #leave as tuple since we'll need to run queries with it
            for lang_id in specific_lang_ids:
                c.execute("SELECT lang_name FROM languages WHERE lang_id=?",(lang_id,))
                self.char_languages.append(c.fetchone()[0])
            if len(choice_lang_ids) > 0:
                c.execute("SELECT lang_id, lang_name FROM languages WHERE lang_id NOT IN (17,18)") #omit druidic and thieves cant
                lang_menu = c.fetchall()
                while len(choice_lang_ids) > 0:
                    print("You have these language proficiences:", end=" ")
                    print(", ".join(self.char_languages))
                    print("You may choose {0} more languages".format(len(choice_lang_ids)))
                    print()
                    for item in lang_menu:
                        if item[1] in self.char_languages:
                            idx = lang_menu.index(item)
                            del lang_menu[idx]
                    for item in lang_menu:
                        print("{0:>2}. {1}".format(item[0], item[1]))
                    print()
                    lang_chosen = int(input("Enter the number of the language you'd like: "))
                    c.execute("SELECT lang_name FROM languages WHERE lang_id=?",(lang_chosen,))
                    self.char_languages.append(c.fetchone()[0])
                    del choice_lang_ids[-1]
                    clear_screen()
            self.char_languages.sort()
            
            #print(all_lang_ids)
            
            
        else:
            raise ValueError("Must have a valid race and background selected before choosing languages. race_id: {0}; bg_id: {1}".format(self.char_race_id, self.char_bg_id))

    def get_trinket(self):
        self.trinket_id = roll_dice(1,100)
        c.execute("SELECT trinket_desc FROM eq_trinkets WHERE trinket_id=?", (self.trinket_id,))
        self.char_trinket = str(c.fetchone()[0])
        self.char_equip.append(self.char_trinket)

    #do not use
    def add_bg(self, bg_id):
        """ this doesn't do anything right now """
        self.char_bg_id = bg_id
        c.execute("SELECT background FROM bg_backgrounds WHERE bg_id=?", (background_id,))
        self.char_bg_name = str(c.fetchone()[0])
        char_skill_profs.append()
    
    
    # OUTPUT
    
    def print_pc_info(self):
        print("Character ID: {0}".format(self.char_id))
        print("Name: {0}".format(self.char_name))
        print("Race/Class/Level: {0} {1} {2}".format(self.char_race_name, self.char_class_name, self.char_lvl))
        print("Size: {0}   Speed: {1}'".format(self.char_size, self.char_speed))
        print("Hit Points: {0}".format(self.char_hp))
        print()
        print("STR {0:>2} ({1})".format(self.char_ability_scores["STR"], pad_modifier(ability_modifiers[self.char_ability_scores["STR"]])))
        print("DEX {0:>2} ({1})".format(self.char_ability_scores["DEX"], pad_modifier(ability_modifiers[self.char_ability_scores["DEX"]])))
        print("CON {0:>2} ({1})".format(self.char_ability_scores["CON"], pad_modifier(ability_modifiers[self.char_ability_scores["CON"]])))
        print("INT {0:>2} ({1})".format(self.char_ability_scores["INT"], pad_modifier(ability_modifiers[self.char_ability_scores["INT"]])))
        print("WIS {0:>2} ({1})".format(self.char_ability_scores["WIS"], pad_modifier(ability_modifiers[self.char_ability_scores["WIS"]])))
        print("CHA {0:>2} ({1})".format(self.char_ability_scores["CHA"], pad_modifier(ability_modifiers[self.char_ability_scores["CHA"]])))
        print("Proficiency Bonus: {0}".format(pad_modifier(self.char_prof_bonus)))
        print("".format())
        #print("RACIAL STUFF".format())
        print("Racial Features")
        print("Languages:", end=" ")
        print(", ".join(self.char_languages))
        if self.char_darkvision > 0:
            print("Darkvision {0}'".format(str(self.char_darkvision)))
        for row in self.char_race_features:
            print("{0}: {1}".format(row[0].upper(), row[1]))
        print("".format())
        #print("CLASS STUFF".format())
        print("".format())
        #print("BACKGROUND STUFF".format())
        print("BACKGROUND: {0}".format(self.char_bg_name))
        if self.char_bg_specialty != None:
            print("{0}: {1}".format(self.bg_spec_title.upper(), self.char_bg_specialty))
        print("PERSONALITY TRAIT: {0}".format(self.char_ptrait))
        print("IDEAL: {0}".format(self.char_ideal))
        print("BOND: {0}".format(self.char_bond))
        print("FLAW: {0}".format(self.char_flaw))
    
    def print_ability_scores(self):
        print("STR " + pad_ability_score(self.char_ability_scores["STR"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["STR"]]) + ")")
        print("DEX " + pad_ability_score(self.char_ability_scores["DEX"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["DEX"]]) + ")")
        print("CON " + pad_ability_score(self.char_ability_scores["CON"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["CON"]]) + ")")
        print("INT " + pad_ability_score(self.char_ability_scores["INT"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["INT"]]) + ")")
        print("WIS " + pad_ability_score(self.char_ability_scores["WIS"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["WIS"]]) + ")")
        print("CHA " + pad_ability_score(self.char_ability_scores["CHA"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["CHA"]]) + ")")
    
