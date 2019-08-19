#!/usr/bin/env python
# coding: utf-8

# In[52]:


from multiprocessing.dummy import Pool as ThreadPool 

import json

import numpy as np

import pandas

import os

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from pymongo import MongoClient

import dns

import dns.resolver
import dns.query
import dns.zone
import dns.query
import dns.tsigkeyring
import dns.update
import dns.zone
import dns.ipv4
import dns.name
import dns.e164
import dns.reversename


# In[53]:


client = MongoClient("mongodb+srv://username:password@lifmarketcluster-zkfv0.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('LiFMarketData')
dbminitemprice = db.MinItemPrice
dbmarketvolume = db.MarketVolume
dbtpvalue = db.TPValue
dbcurrentmarketdata = db.CurrentMarketData
dbtimestamps = db.TimeStamps


# In[54]:


import requests
from IPython.display import clear_output

s = requests.session()
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='PHPSESSID',value='dbb6877fcf212d9da645c2f511988df5')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='GMT_bias',value='360')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='charId',value='588844')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='charId',value='588844',rest={'HttpOnly': True},secure=True)
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='.lif.online',name='charId',value='588844',rest={'HttpOnly': True},secure=True)
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='market_charId',value='588844')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='market_msg',value='Ok.+Succeeded')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='market_tradePostId',value='387')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='market_userId',value='424622')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='market_worldId',value='eu-big')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='token',value='Vzo0MjQ2MjI6MTU2NjQ4MDMzMzo0OWM0YWJjMzAyMzhkYjVmMzIxOTllMjk3MDMyMDAxZDg0NDA3ZjMy')
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='region-eu.lif.online',name='token',value='Vzo0MjQ2MjI6MTU2NjQ4MDMzMzo0OWM0YWJjMzAyMzhkYjVmMzIxOTllMjk3MDMyMDAxZDg0NDA3ZjMy',rest={'HttpOnly': True},secure=True)
s.cookies.set_cookie(cookie_obj)
cookie_obj = requests.cookies.create_cookie(domain='.lif.online',name='token',value='Vzo0MjQ2MjI6MTU2NjQ4MDMzMzo0OWM0YWJjMzAyMzhkYjVmMzIxOTllMjk3MDMyMDAxZDg0NDA3ZjMy',rest={'HttpOnly': True},secure=True)
s.cookies.set_cookie(cookie_obj)

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }


# In[43]:




#Fetches API, captures datetime, removes unwanted keys and values, saves the result to current.json.

from datetime import datetime
filename = datetime.now().strftime('%Y%m%d%H%M%S')
print(filename)

response = requests.get("https://region-eu.lif.online/market/market-api.php?list=itemOnSale&itemId=99999", timeout=500, cookies=s.cookies, headers=headers)
response.status_code

resp = response.json()

data = resp['data']

print(len(data))




for i in range(len(data)):
      currdict = data[i]
      currdict.pop('ItemID');
      currdict.pop('LotID');
      currdict.pop('ContainerID');
      currdict.pop('CustomText');
      currdict.pop('CreatedRegionID');
      currdict.pop('BlueprintID');
      currdict.pop('HasEffects');
      currdict.pop('Magnitude');
      currdict.pop('Effect_name');
      currdict.pop('Durability');
      currdict.pop('CreatedDurability');
      currdict.pop('SellerCharID');
      currdict.pop('TradePostID');
      currdict.pop('BasePrice');
      currdict.pop('FaceImage'); 
      currdict.pop('inQueue');
      currdict.pop('Effects');
      
with open(os.path.join('LiFMarketDatabase/', "Current"), "w") as json_file:
    json.dump(data, json_file)
    


# In[44]:


dbts = {Timestamp:filename}

dbtimestamps.insert_one(dbts)
dbcurrentmarketdata.delete_many({})
dbcurrentmarketdata.insert_many(data)


# In[45]:


# Create list of lowest price, above 50ql, for each item in the list. If it exists.

item_list = ("Arrow", "Bodkin Arrow", "Broadhead Arrow", "Dull Arrow", "Fire Arrow", "Firework Arrow", "Wooden Arrow", "Bolt", "Dull Bolt", "Firework Bolt", "Heavy Bolt", "Wooden Bolt", "Heavy Chainmail Gauntlets", "Heavy Chainmail Greaves", "Heavy Chainmail Helm", "Heavy Chainmail Leggings", "Heavy Chainmail Tunic", "Heavy Chainmail Vambraces", "Light Chainmail Gauntlets", "Light Chainmail Greaves", "Light Chainmail Helm", "Light Chainmail Leggings", "Light Chainmail Tunic", "Light Chainmail Vambraces", "Regular Chainmail Gauntlets", "Regular Chainmail Greaves", "Regular Chainmail Helm", "Regular Chainmail Leggings", "Regular Chainmail Tunic", "Regular Chainmail Vambraces", "Royal Chainmail Gauntlets", "Royal Chainmail Greaves", "Royal Chainmail Helm", "Royal Chainmail Leggings", "Royal Chainmail Tunic", "Royal Chainmail Vambraces", "Heavy Leather Breastplate", "Heavy Leather Gauntlets", "Heavy Leather Greaves", "Heavy Leather Helm", "Heavy Leather Leggings", "Heavy Leather Vambraces", "Novice Leather Breastplate", "Novice Leather Gauntlets", "Novice Leather Greaves", "Novice Leather Helm", "Novice Leather Leggings", "Novice Leather Vambraces", "Regular Leather Breastplate", "Regular Leather Gauntlets", "Regular Leather Greaves", "Regular Leather Helm", "Regular Leather Leggings", "Regular Leather Vambraces", "Royal Leather Breastplate", "Royal Leather Gauntlets", "Royal Leather Greaves", "Royal Leather Helm", "Royal Leather Leggings", "Royal Leather Vambraces", "Heavy Padded Gauntlets", "Heavy Padded Greaves", "Heavy Padded Helm", "Heavy Padded Leggings", "Heavy Padded Tunic", "Heavy Padded Vambraces", "Novice Padded Gauntlets", "Novice Padded Greaves", "Novice Padded Helm", "Novice Padded Leggings", "Novice Padded Tunic", "Novice Padded Vambraces", "Regular Padded Gauntlets", "Regular Padded Greaves", "Regular Padded Helm", "Regular Padded Leggings", "Regular Padded Tunic", "Regular Padded Vambraces", "Royal Padded Gauntlets", "Royal Padded Greaves", "Royal Padded Helm", "Royal Padded Leggings", "Royal Padded Tunic", "Royal Padded Vambraces", "Full Plate Breastplate", "Full Plate Gauntlets", "Full Plate Greaves", "Full Plate Helm", "Full Plate Leggings", "Full Plate Vambraces", "Half Plate Breastplate", "Half Plate Gauntlets", "Half Plate Greaves", "Half Plate Helm", "Half Plate Leggings", "Half Plate Vambraces", "Iron Plate Breastplate", "Iron Plate Gauntlets", "Iron Plate Greaves", "Iron Plate Helm", "Iron Plate Leggings", "Iron Plate Vambraces", "Royal Full Plate Breastplate", "Royal Full Plate Gauntlets", "Royal Full Plate Greaves", "Royal Full Plate Helm", "Royal Full Plate Leggings", "Royal Full Plate Vambraces", "Heavy Scale Gauntlets", "Heavy Scale Greaves", "Heavy Scale Helm", "Heavy Scale Leggings", "Heavy Scale Tunic", "Heavy Scale Vambraces", "Light Scale Gauntlets", "Light Scale Greaves", "Light Scale Helm", "Light Scale Leggings", "Light Scale Tunic", "Light Scale Vambraces", "Regular Scale Gauntlets", "Regular Scale Greaves", "Regular Scale Helm", "Regular Scale Leggings", "Regular Scale Tunic", "Regular Scale Vambraces", "Royal Scale Gauntlets", "Royal Scale Greaves", "Royal Scale Helm", "Royal Scale Leggings", "Royal Scale Tunic", "Royal Scale Vambraces", "Buckler Shield", "Heater Shield", "Heavy Heater Shield", "Heavy Iron Shield", "Heavy Kite Shield", "Heavy Targe Shield", "Iron Round Shield", "Kite Shield", "Pavise", "Primitive Shield", "Small Kite Shield", "Targe Shield", "Tower Shield", "Blacksmith's Outfit", "Breeder's Outfit", "Carpenter's Outfit", "Cook's Outfit", "Crown of the Eternal Watchman", "Decorated Clothes", "Engineer's Outfit", "Fur Hat", "Golden Mark", "Herbalist's Outfit", "Monk's Outfit", "North Rags", "Primitive Boots", "Rags", "Simple Clothes", "Steppe Hat", "Steppe Rags", "Stonecutter's Outfit", "Svefnibrann", "Thousand-Strong Host", "Tiara of the Sleepless Eye", "Tiara of the Sleepless Eye (red)", "Wool Hat", "Wristbands", "Archimankur's Outfit", "Banner", "Banner", "Black Robe", "Checker Capelet Mantle", "Elegant Blue Cloak", "Elegant Purple Cloak", "Elegant Red Cloak", "Eminent Cloak", "Fancy Decorated Outfit", "Fancy Peasant's Outfit", "Jarl's Clothes", "Konung's Outfit", "Liege's Garb", "Makthrid's Outfit", "Mantle Gold and White Capelet", "Mantle Red Capelet", "Merchant's Cloak", "Monarch's Dress", "Noble Simple Clothes", "Northern Garb", "Pilgrim Outfit", "Pioneer's Robe", "Robe of Believer", "Royal Outfit", "Runic Tunic", "Strelets' Garb", "Tabard", "Villein's Clothes", "White Robe", "Adrenaline Cocktail", "Aquila Wings Cocktail", "Bull's Strength Cocktail", "Double Blood (Antidote) Cocktail", "Iron Will Cocktail", "Refreshing Cocktail", "Swift Limbs Cocktail", "Swift Mind Cocktail", "Toughness Cocktail", "Breathtaker Poison", "Eternal Sleep Poison", "Grave Weight Poison", "Lungs of Stone Poison", "Numbing Poison", "Poison", "Flavour", "Flux", "Naphtha", "Jug", "Primitive Cup", "Backpack", "Bag", "Pouch", "Sack", "Primitive Sewing Tools", "Weaver's Toolkit", "Carpenter's Toolkit", "Jeweler's Toolkit", "Mortar and Pestle", "Bull", "Calf", "Cow", "Hairy Bull", "Hairy Calf", "Hairy Cow", "Hairy Heifer", "Heifer", "Old Bull", "Old Cow", "Old Hairy Bull", "Old Hairy Cow", "Pregnant Cow", "Pregnant Hairy Cow", "Hardy Warhorse", "Heavy Warhorse", "Royal Warhorse", "Spirited Warhorse", "Warhorse", "Colt", "Courier Horse", "Foal", "Horse", "Old Horse", "Old Stallion", "Pregnant Horse", "Stallion", "Boar", "Mangalica Boar", "Mangalica Pig", "Mangalica Piglet", "Mangalica Pigling", "Old Boar", "Old Mangalica Boar", "Old Mangalica Pig", "Old Pig", "Pig", "Piglet", "Pigling", "Pregnant Mangalica Pig", "Pregnant Pig", "Mountain Poddy", "Mountain Ram", "Mountain Sheep", "Mountain Yonling", "Old Mountain Ram", "Old Mountain Sheep", "Old Ram", "Old Sheep", "Poddy", "Pregnant Mountain Sheep", "Pregnant Sheep", "Ram", "Sheep", "Yonling", "Chick", "Chicken", "Little Rabbit", "Old Chicken", "Old Rabbit", "Rabbit", "Tamed Moose", "Beer", "Cider", "Mead", "Wine", "Apple Pie", "Baabaa Couscous ", "Beer pancakes", "Beer Pie", "Cookies", "Cottage Pie", "Fat Fish Soup", "Fish Madness", "Minestrone", "Mixed Porridge", "Mumkin Borscht", "Oatmeal, sir!", "Pea Soup", "Peceno Veprevo Koleno", "Pumpernickel", "Samsa", "Shchi", "Solyanka", "Stuffed Rabbit", "Vegetable stew", "Waterzooi", "Yorkshire Pudding", "Bacon", "Boiled Chicken", "Boiled Eggs", "Boiled Potatoes", "Bread", "Fried Fish", "Fried Meat", "Porridge", "Apple Buns", "Beef Bouillon", "Beef Steak", "Fish Pottage", "Lamb Bouillon", "Lean Pottage", "Pizza", "Pork Bouillon", "Pork with Vegetables", "Vegetable Patty", "Vegetable Patty", "Cabbage", "Carrot", "Peas", "Small Onion", "Apple", "Dark Honey", "Edible Berries", "Edible Taproot", "Grapes", "Green Onion", "Green Peas", "Honey", "Milk", "Nuts", "Onion", "Sugar Carrot", "White Cabbage", "White Honey", "Yellow Honey", "Berries in Honey", "Cheese", "Crispy Chicken", "Fish Patty", "Fried Eggs", "Meat Patty", "Meat Stew", "Potato with Mushrooms", "Sausage", "Baguette", "Borscht", "Bubble and squeak", "Cake with Giblets", "Chebureki", "Cheese Buns", "Chorba", "East Fish Soup", "Egg Salad", "Fish Bullion", "Fish Soup", "Greatberry Pie", "Highlander's Sausage", "Lager", "Lean Stew", "Mushrooms Stew", "North Fish Soup", "Oat Stout", "Rassolnik", "Ravioli", "Red Ale", "Sardine Stew", "South Fish Soup", "West Fish Soup", "White Beer", "Amulet from Illa-Newydd", "Exceptional Gold and Silver Amulet", "Exceptional Gold and Silver Ring", "Gold and Silver Amulet", "Gold and Silver Ring", "Gold Diamond Ring", "Gold Emerald Ring", "Gold Jeweled Necklace", "Gold ring", "Gold Sapphire Ring", "Pioneer's Amulet", "Silver Amethyst Ring", "Silver Garnet Ring", "Silver Jeweled Necklace", "Silver Ring", "Silver Ruby Ring", "Animal Skull", "Chest Pendulum", "Chieftain's Helm", "Chieftain's Knee Pad", "Clawed Paw", "Crow Charm", "Dead Fetus Charm", "Handlace", "Hunter's Mask", "Impious Chieftain's Symbol", "Inhuman Skull", "Raven Amulet", "Shrunken Head", "Skull Mask", "Unholy Eternity Sign", "Unholy Face of Anger", "Unholy Lung Vision", "Unholy Sign of Death", "Unholy Sleeping Stone", "Unholy Tree of Life", "Witch Braid", "Witch Skull", "Door Module", "Gate Module", "Window Module", "Empty Bottle", "Animal Trap", "Anvil", "Case-hardened Chainmail", "Case-hardened Metal Band", "Case-hardened Metal plate", "Case-hardened Metal Sheet", "Case-hardened Scale strip", "Case-hardened Small metal plate", "Chainmail", "Horse Armor", "Lock", "Metal Band", "Metal Components", "Metal plate", "Metal Sheet", "Nails", "Scale strip", "Small metal plate", "Toughened Chainmail", "Toughened Metal Band", "Toughened Metal plate", "Toughened Metal Sheet", "Toughened Scale strip", "Toughened Small metal plate", "Wire", "Naphtha Barrel", "Naphtha Nail Barrel", "Stone Ammo", "Lamp", "Pipe", "Siege Torch", "Torch", "Rough Thick Dried Hide", "Rough Thin Dried Hide", "Soft Thick Dried Hide", "Soft Thin Dried Hide", "Thick Dried Hide", "Thin Dried Hide", "Rough Thick Leather", "Soft Thick Leather", "Thick Leather", "Rough Thin Leather", "Soft Thin Leather", "Thin Leather", "Leather strips", "Bone Glue", "Edible parts", "Brick", "Clay Tile", "Marble Plate", "Shaped Granite", "Shaped rock", "Hank of Coarse Wool", "Hank of Soft Wool", "Hank of Wool", "Coarse Wool Cloth", "Soft Wool Cloth", "Wool Cloth", "Bandage", "Hank of Linen", "Hank of Silk", "Linen Cloth", "Linen Rope", "Silk Cloth", "Simple Cloth", "Simple Rope", "Barley Malt", "Brewed Honey", "Fermented Apple Juice", "Fermented Grape", "Malt", "Oat Malt", "Rye Malt", "Wheat Malt", "Crushed Oat", "Flour", "Rye Flour", "White Flour", "Coarse Wool", "Soft Wool", "Wool Pack", "Flax Fibers", "Silk Filaments", "Butter", "Dough", "Clay Anvil Form", "Glass", "Gypsum Mortar", "Lime Mortar", "Mortar", "Unfired Brick", "Unfired Clay Tile", "Unfired Jug", "Unfired Masterwork Vase", "Unfired Urn", "Unfired Vase", "Case-hardened Iron Bar", "Case-hardened Steel Bar", "Case-hardened Vostaskus Bar", 
                     "Iron Bar", "Steel Bar", "Vostaskus Bar", "Gold Bar", "Silver Bar", "Toughened Iron Bar", "Toughened Steel Bar", "Toughened Vostaskus Bar", "Copper Bar", "Irregular Alloy", "Case-hardened Iron Ingot", "Case-hardened Steel Ingot", "Case-hardened Vostaskus Ingot", "Iron Ingot", "Steel Ingot", "Vostaskus Ingot", "Gold Ingot", "Silver Ingot", "Toughened Iron Ingot", "Toughened Steel Ingot", "Toughened Vostaskus Ingot", "Copper Ingot", "Irregular Alloy Ingot", "Lump of Iron", "Lump of Steel", "Lump of Vostaskus Steel", "Gold Nugget", "Silver Nugget", "Lump of Copper", "Lump of Irregular Alloy", "Breathtaker Preparation", "Eternal Sleep Preparation", "Grave Weight Preparation", "Lungs of Stone Preparation", "Numbing Preparation", "Poisonous Preparation", "Adrenaline Preparation", "Aquila Wings Preparation", "Bull's Strength Preparation", "Double Blood (Antidote) Preparation", "Iron Will Preparation", "Refreshing Preparation", "Swift Limbs Preparation", "Swift Mind Preparation", "Toughness Preparation", "Building Kit", "Large Repair Kit", "Medium Repair Kit", "Small Repair Kit", "Explosive", "Large Warfare Kit", "Medium Warfare Kit", "Siege Ladder Kit", "Small Warfare Kit", "Charcoal", "Handle", "Little Boards", "Snare Trap", "Wheel", "Alchemical Glassware", "Distiller", "Codfish", "Herring", "Pike", "Salmon", "Sardine", "Trout", "Beef", "Marbled Beef", "Marbled Pork", "Pork", "White Meat", "White Meat", "Game Meat", "Lamb", "Mutton", "Intestines", "Animal Calculi", "Blinded Eye", "Bone Meal", "Crystalized Bile", "Digested Feather", "Glowing Urine", "Odd Claw", "Overgrown Parasite", "Piece of Diseased Hide", "Purbon", "Strange Muscle", "Uncommon Tendon", "Bear Hide", "Big Hide", "Wolf Hide", "Boar Hide", "Fur", "Cowhide", "Pigskin", "Rough Cowhide", "Rough Pigskin", "Rough Sheepskin", "Sheepskin", "Big Bear Head", "Big Deer Head", "Big Moose Head", "Boar Head", "Bones", "Bull Head", "Claws", "Dung", "Feathers", "Horn", "Tusk", "Wolf Head", "Wild Barley", "Wild Oat", "Wild Rye", "Wild Wheat", "Barley", "Big Potato", "Cabbage Seeds", "Carrot Seeds", "Egg", "Mushroom", "Oat", "Onion Seeds", "Potato", "Rye", "Sugar Carrot Seeds", "Wheat", "White Cabbage Seeds", "Flax Seeds", "Flax stem", "Rich Flax Seeds", "Silkworm Cocoon", "Straw", "Amethyst", "Cracked Gem", "Diamond", "Emerald", "Garnet", "Raw Gem", "Rough Gem", "Ruby", "Sapphire", "Aktashite", "Bixbyite", "Chrysoberyl", "Euclase", "Gahnite", "Humite", "Kutnohorite", "Meionite", "Parsonsite", "Scolecite", "Tellurite", "Urea", "granite_ter2_id_12", "Fertile Soil", "Forest Soil", "Soil", "Brimstone", "Clay", "Flint Stone", "Granite", "Gypsum", "Limestone", "Marble", "Rock", "Rocksalt", "Sand", "Slate", "Snow", "Acerba Moretum", "Adipem Nebulo", "Albus Viduae", "Aquila Peccatum", "Aureus Magistrum", "Bacce Hamsa", "Burmenta Wallo", "Caeci Custos", "Chorea Iram", "Curaila Jangha", "Curva Manus", "Desertus Smilax", "Dulcis Radix", "Dustali Krabo", "Errantia Ludaeo", "Fakha Rudob", "Falcem Malleorum", "Fassari Tolge", "Filia Prati", "Fohatta Torn", "Fuskegtra Xelay", "Gortaka Messen", "Gratias Sivara", "Hallatra Kronye", "Holmatu Stazo", "Huryosa Gulla", "Ital Iranta", "Jenaro Vannakam", "Jukola Beshaar", "Kacaro Vilko", "Kaleda Mesgano", "Kalya Nori", "Khalari Gratsi", "Kromenta Salicia", "Kurupa Andhere", "Kyasaga Sherl", "Laster Kutta", "Mala Fugam", "Mauna Boba", "Memen Anik", "Mons Bastardus", "Muncha Vana", "Murkha Bola", "Naraen Pandanomo", "Nequissimum Propodium", "Nocte Lumen", "Oscularetur", "Pecuarius Ventus", "Persetu Hara", "Petra Stellam", "Phlavar Pharest", "Pitaku Koro", "Pungentibus Chorea", "Rakta Stema", "Remerta Poskot", "Ripyote Quamisy", "Rosa Kingsa", "Saltare Diabolus", "Sapienta Mantis", "Sarmento Gaute", "Suryodaya bhagya", "Topasa Maidana", "Uliya Sundara", "Utrokka Khuru", "Vertato Zonda", "Viridi ursae", "Plant Fiber", "Copper Ore", "Iron Ore", "Gold Ore", "Silver Ore", "Fresh water", "Salt water", "Stale Water", "Hardwood Billet", "Softwood Billet", "Amberwood Board", "Hardwood Board", "Softwood Board", "Whitewood Board", "Amberwood Building Log", "Building Log", "Whitewood Building Log", "Apple Sprout", "Aspen Sprout", "Birch Sprout", "Elm Sprout", "Grape Vine", "Hazel Sprout", "Juniper Sprout", "Maple Sprout", "Mulberry Sprout", "Oak Sprout", "Pine Sprout", "Spruce Sprout", "Wild Grape Vine", "Bark", "Branch", "Sinner's Head", "Believer's Cooking Pot", "Cooking Pot", "Primitive Cooking Pot", "Believer's Fishing Pole", "Fishing Pole", "Primitive Fishing Pole", "Believer's Hammer", "Blacksmith's Hammer", "Primitive Hammer", "Mallet", "Believer's Hatchet", "Hatchet", "Primitive Axe", "Believer's Knife", "Knife", "Primitive Knife", "Skinning Knife", "Believer's Pickaxe", "Hardened Steel Pickaxe", "Knool's Pickaxe", "Pickaxe", "Primitive Pickaxe", "Believer's Saw", "Primitive Saw", "Saw", "Believer's Shovel", "Primitive Shovel", "Shovel", "Believer's Sickle", "Knool's Sickle", "Primitive Sickle", "Sickle", "Believer's Crucible and Tongs", "Crucible and Tongs", "Primitive Crucible and Stick", "Glassblower's Toolkit", "Composite Bow", "Knool's Bow", "Longbow", "Short Bow", "Simple Bow", "Arbalest", "Heavy Crossbow", "Light Crossbow", "Bastard Sword", "Big Falchion", "Knight Sword", "Practice Bastard", "Decorated Jousting Lance", "Jousting Lance", "Lance", "Battle Axe", "Knool's Axe", "Nordic Axe", "Practice Axe", "War Axe", "Cudgel", "Flanged Mace", "Morning Star", "War Pick", "Falchion", "Gross Messer", "Light Sabre", "Nordic Sword", "Practice Sword", "Scimitar", "Long Pike", "Medium Pike", "Short Pike", "Balanced Staff", "Glaive", "Guisarme", "Partisan", "Pitchfork", "Pollaxe", "Staff", "War Scythe", "Awl Pike", "Bec de Corbin", "Boar Spear", "Spear", "Firework Pot", "Javelin", "Naphtha Pot", "Snowball", "Stones", "Throwing Axe", "Throwing Knife", "Bardiche", "Broad Axe", "Knool's Bear Axe", "Practice Great Axe", "Maul", "Practice Maul", "Sledge Hammer", "Claymore", "Estoc", "Flamberge", "Knool's Chieftain Sword", "Practice Longsword", "Zweihaender", "Sling", "Ancient Scroll", "Apprentice Decorator's Kit", "Baromsag", "Horse Spirit Badge", "Indulgence", "Lesser Battle Totem", "Master Decorator's Kit", "Novice Decorator's Kit", "Old Rusty Ring", "Savage Trophy", "Shrunken Gottlung's head", "Siege Totem", "Slave")

pricedict = {}
checkprice = []
pricedict.update({'TimeStamp':filename})

for nval in item_list:
    for index, value in enumerate(data):
        if value['Name'] == nval:
            if int(value['Quality']) >= 50:
                checkprice.append(int(value['CoinPrice']))             
            
    if len(checkprice) >= 1:
        mval = min(checkprice)
        pricedict.update({nval:mval})
        checkprice = []

        
with open(os.path.join('LiFMarketDatabase/', "itemlistprices"), "w") as json_file:
    json.dump(pricedict, json_file)

#The Damage: pricedict = a list of the lowest price for items above 50ql for a corresponding item name. listed as item_name : lowest price
#Will be used for plotting 


# In[46]:



dbminitemprice.insert_one(pricedict)


# In[47]:


# Create a list of dicctionaries of unique tradepost names, and timestamp.

#Clear all previous data
tpnamesdict = {}
tpnames = []
tpnfin = []

#Create Timestamp
timestamp = {'TimeStamp':filename}

#Add timestamp, and starting value, to beigin search.
tpnfin.append(timestamp)
tpnamesdict.update({'TradePostName':data[0]['TradePostName']})
tpnames.append(data[0]['TradePostName'])

#Searches list of dictionaries for unique values and adds them to tpnames.
for index, value in enumerate(data):
    for tpval in tpnames:
        if value['TradePostName'] == tpval:
            break
    if value['TradePostName'] != tpval:
        tpnames.append(value['TradePostName'])
    
#Sort list A to Z.        
tpnames.sort()

#Add list of dictionaries to tpnfin, to facilitate future searhes.
for tpnval in tpnames:
    tpfinval = tpnval
    tpndict = {'TradePostName':tpfinval}
    tpnfin.append(tpndict)

with open(os.path.join('LiFMarketDatabase/', "tradepostnames"), "w") as json_file:
    json.dump(tpnfin, json_file)
#Write file to current tradepost names.
    
#The damage: tpnfin = list of dictionaries including, timestamp at index 0, and unique tradepost names pulled from data. 
#tpnames = the list of unique tradepost names with no identifiesrs/


# In[48]:


#This module is to create and upload item volume to the database.

addvolume = 0
itemvolume = {}
itemvolume.update({'TimeStamp':filename})

for naval in item_list:
    for index, value in enumerate(data):
        if value['Name'] == naval:
            addvolume = addvolume + int(value['Quantity'])
            
    if addvolume >= 1:
        itemvolume.update({naval:addvolume})
        addvolume = 0
    else:
        addvolume = 0


            


# In[49]:


dbmarketvolume.insert_one(itemvolume)


# In[50]:


#This module calculates Tradepost Value

addvalue = 0
tpvalue = {}
tpvalue.update({'TimeStamp':filename})

for tpnval in tpnames:
    for index, value in enumerate(data):
        if value['TradePostName'] == tpnval:
            addvalue = addvalue + int(value['CoinPrice'])
            
    tpvalue.update({tpnval:addvalue})
    addvalue = 0
    


# In[51]:


dbtpvalue.insert_one(tpvalue)

