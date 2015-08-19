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
        self.char_race_name = None
        self.char_race_features = None
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

    def print_ability_scores(self):
        print("STR " + pad_ability_score(self.char_ability_scores["STR"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["STR"]]) + ")")
        print("DEX " + pad_ability_score(self.char_ability_scores["DEX"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["DEX"]]) + ")")
        print("CON " + pad_ability_score(self.char_ability_scores["CON"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["CON"]]) + ")")
        print("INT " + pad_ability_score(self.char_ability_scores["INT"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["INT"]]) + ")")
        print("WIS " + pad_ability_score(self.char_ability_scores["WIS"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["WIS"]]) + ")")
        print("CHA " + pad_ability_score(self.char_ability_scores["CHA"]) + " (" + pad_modifier(ability_modifiers[self.char_ability_scores["CHA"]]) + ")")
    

    
    # RACE
    def choose_race(self):
        """ allow the user to select a race """
        c.execute("SELECT race_id, race_name, bonus_text FROM races")
        race_list = c.fetchall()
        for race in race_list:
            race_pk = race[0]
            race_name = str(race[1])
            race_bonus_text = str(race[2])
            print(str(race_pk) + ". " + race_name + ": " + race_bonus_text)
        self.char_race_id = int(input("Enter the number of the race you'd like: "))
        c.execute("SELECT race_name FROM races WHERE race_id=?", (self.char_race_id,))
        self.char_race_name = str(c.fetchone()[0])
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
        self.char_size = int(c.fetchone()[0])
    
    def get_race_features(self):
        c.execute("SELECT feature_name, feature_text FROM race_features WHERE race_id=?",(self.char_race_id,))
        results = c.fetchall()
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
        for bg in bg_list:
            print(bg[0] + " " + str(bg[1]))
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
        """  """
    
    def apply_bg_equip(self):
        """  """
    
    # CLASS
    
    
    
    
    
    # OTHER

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
    
    
