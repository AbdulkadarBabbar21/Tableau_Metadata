# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:08:25 2021

@author: ababbar
"""

import pandas as pd
from tableau_extract import get_login, get_html_dashbrd, get_load_dashbrd,\
                        get_filter_name, get_filter_value, get_parameter_value, get_words_frm_html,get_parameter_name

from tableau_extract import text_cleaning, remove_element

from credentials_okta import webdriver_path,okta_user_id,okta_user_passwrd
import time

def init_result_dict():
    result_dict = {}
    result_dict['WorkBook']  = ''
    result_dict['dashboard_url']= ''
    result_dict['filter_name'] = ''
    result_dict['filter_values'] = ''
    result_dict['parameter_name'] = ''
    result_dict['parameter_values'] = ''
    result_dict['Keywords'] = ''
    result_dict['final']  = ''
    return(result_dict)

doc = 'https://docs.google.com/spreadsheets/d/1JJUD8iv9DduJT4txmebDyRepXP_lejWEQvnUs9FqXos/edit?usp=sharing'

urls = ['https://tableau.discovery.com/#/views/ContinuousPlay/ContinuousPlay?:iid=1',
        'https://tableau.discovery.com/#/views/DailyContentBlast/DailyContentSummary?:iid=1',
        'https://tableau.discovery.com/#/views/UsageDashboard/Datasources-Workbooks?:iid=1',
        'https://tableau.discovery.com/#/views/HourlyDeviceTrends/HourlyDeviceTrends'
        ]

'''
urls=['https://tableau.discovery.com/#/views/SelfServiceContentTracker/CumulativeContentBuild',
      'https://tableau.discovery.com/#/views/MonthlyContentBlast_16123018698830/MonthlyContentSummary',
'https://tableau.discovery.com/#/views/SelfServiceContentTracker/NewSubsContribution',
'https://tableau.discovery.com/#/views/SelfServiceContentTracker/Overview',
'https://tableau.discovery.com/#/views/DailySeriesReach-GeneralAccess/SeriesTracker']

'''

series_name=['eating america with anthony anderson', 'princess diana: tragedy or treason?', "wolfgang puck's cooking class", 'most evil', 'halloween baking championship', 'easy chinese', 'the interrogation room', 'build it bigger', 'great global clean up', 'dam', 'holiday gingerbread showdown', 'amish haunting', '8 movie makers', 'breaking amish', 'the great american groom-a-long', 'ghost adventures aftershocks', 'klondike', 'kitchen impossible', '3 axles and a baby', 'the diamond collar', 'hotel showdown', 'my crazy birth story', 'bahamas life', 'escaped', 'off limits', 'celebrities at home', 'madeleine mccann: an id murder mystery', 'inseparable: joined at the head', '20-minute pregnancy workout', 'killer instinct with chris hansen', 'salvage dawgs', '90 day journey: angela & michael', 'robert durst: an id murder mystery', 'the treasure hunters', 'five star secrets', 'giada on the beach', 'killing fields', '2 bathrooms, no bedroom', 'loch ness monster: new evidence', 'moon machines', 'unmasked', 'the 685lb teen', 'naked and afraid', 'property brothers: linda and drew say i do', 'jessica chambers: an id murder mystery', 'one small step', 'puppy bowl', '3 weddings and a robert', 'michael jackson: searching for neverland', 'madman of the sea', 'frozen in time', 'la ink', "welcome to sweetie pie's", 'wild times', 'indoors out', '5-year storm, part 1', 'horizon: why did i go mad?', 'alien highway', 'beasts of the bayou', 'what the faqs', 'honor flight heroes', 'natural world: animal house', 'apocalypse preppers', 'predators up close', 'predator at large', 'truth behind the moon landing', 'ghosts of shepherdstown', 'expedition unknown', 'sin city justice', 'betrayed', 'martha knows best', '90 day journey: molly & luis', 'city vs. burbs', '4th of july special', 'extra virgin', 'cousins on call', 'wedding island', 'gypsy sisters', 'saving grace', '21st century bathroom', 'kitchen expedition', 'nfl super stadiums', 'man, cheetah, wild', 'my pregnant husband', 'world war ii: witness to war', 'rehab addict: detroit', 'hoarding: buried alive', 'never say goodbye', 'living with maneaters', 'intervention', 'iron chef showdown', 'black and blue', 'my tiny terror', 'our wild life', '8 landscapes in 8 hours', 'new subs contribution by day', '90 day pillow talk: the other way', 'vegas rat rods', 'britney ever after', 'street outlaws: new orleans', 'how (not) to kill your husband', 'property brothers at home', 'flip or flop', 'cold hearted', 'mega dens', 'national parks top 10', 'amba: the russian tiger', 'row solo', 'cold case files', 'strange love', "mark & derek's excellent flip", 'quick fix meals with robin miller', 'off the hook: extreme catches', 'burger land', 'selling new york', 'how do they do it?', 'living a nightmare', 'adnan syed: innocent or guilty?', 'new subs contribution', "bill bailey's jungle hero", 'resort rescue', 'secrets of a restaurant chef', '90 day: bares all', '60 days in', 'american diner revival', 'paranormal lockdown', 'along for the bride', 'red devil racers', 'the vanilla ice project', 'party animals', 'outrageous acts of science', '16 minute meals: italian', 'natural world: meet the monkeys', 'curvy brides', 'masters of flip', '2-in-1', '16-minute tex mex', 'cold river cash', "home town: ben's workshop", 'still a mystery', 'the mothman sightings', 'horizon: being transgender', 'cats of claw hill', 'ocean warriors', 'outback opal hunters', "world's smallest woman: meet jyoti", 'last seen alive', 'jfk: the lost tapes', 'last american cowboy', 'kodiak', 'the story of plastic', 'donna decorates dallas', 'hello world!', 'how do animals do that?', 'inspire a difference', 'extreme makeover: home edition', 'my big fat fabulous life', 'building belushi', 'island hunters', 'houston beauty', 'horizon: how to build an astronaut', 'own spotlight: where do we go from here?', 'the ambush cook', 'extra yardage', 'prophets of science fiction', 'animal cops phoenix', 'expedition mungo', 'christina on the coast', 'btk: chasing a serial killer', 'deadly engineering', 'double cross', 'chef hunter', 'rise of the warrior apes', 'the haunted: death rises', 'bakers vs. fakers', 'quints by surprise', 'scaled', 'marrying millions', '7 people with 7 opinions', 'the steve irwin story', 'buying the bayou', 'invisible worlds', 'turkey day sunny’s way', 'wwii: masters of war', 'buddy valastro: road to recovery', 'chrome underground', 'hometown homicide: local mysteries', 'polar bear - spy on the ice', 'ultimate recipe showdown', 'who do you think you are?', 'construction intervention', 'deadline: crime with tamron hall', 'the boston strangler: the hunt for a killer', 'the murder of laci peterson', 'say yes to the dress: uk', 'junk food flip', 'gator boys', '16-minute meals: cowboy style', 'battlebots', 'cajun aces', 'seeking sister wife', 'how the universe works', 'american monster', 'chopped after hours', '30 minute renovations', 'storm chasers', 'gardening by the yard', 'guilty rich', '5 million dollar season', "inside the vatican's vault", 'horizon: dancing in the dark - the end of physics?', 'designing for the sexes', 'animal nation with anthony anderson', "don't blink", 'mysteries of the outdoors', 'susan powell: an id murder mystery', '25 ingredients or less', 'beach flip', 'in orbit - how satellites rule our world', 'evil, i', 'american muscle', "rachael ray's tasty travels", 'sons of winter', 'diabolical (2013)', 'tiger - spy in the jungle', 'harry & meghan: a royal romance', 'fix my fail', 'life after: chernobyl', 'southwest of salem', '3-d printers and more', 'this wild life', 'bbq with bobby flay', 'expedition unknown: hunt for the yeti', 'carspotting', 'culinary genius', 'secrets of the morgue', 'into the wild with gordon buchanan', 'operation thai cave rescue', 'launch to date cumulative stream starts', "crikey! it's the irwins", 'miami ink', 'save my skin', 'nightwatch nation', 'why we hate', 'wildlife sos', 'i, witness', 'heat seekers', '90 day fiancé: happily ever after?', 'wild costa rica', 'property virgins', 'mystery of the lost islands', 'dead of night (2013)', 'contact', 'outrageous holiday houses', '19 designers and 1 fanuka', 'flipping moms', 'the spouse house', 'hometown homicide', "i'm pregnant and...", "i'd kill for you", 'log cabin living', 'aehi', 'super dad', 'secret life of money', 'sex sent me to the slammer', 'secrets of the lost', '4 women and a funeral', 'who the (bleep)...', 'alaska off the grid', 'all-star academy', 'food network star', 'shipwreck secrets', 'boy meets grill', 'leave it to niecy', 'fear not with iyanla vanzant', 'i want that wedding', 'black women own the conversation', 'sugar dome', 'brother husbands', 'hot & heavy', '16-minute meals: summer', 'people magazine investigates: cults', 'wild west', 'video completion', "gold rush: dave turin's lost mine", 'love it or list it australia', 'bondi vet', 'suspicious minds', 'armed & ready', "ayesha's home kitchen", '6 months later', 'mysteries of the abandoned: animal uprising', '3-2-1 blast off!', '90 day journey: mike & natalie', 'walking with elephants', 'american chopper', 'horizon: are we still evolving?', 'toughest race on earth: iditarod', 'finding bigfoot', 'cold blood', 'deadly recall', 'hair goddess', 'super factories', 'the colony', "gordon's great escape", "samantha brown's asia", '5 ingredient fuel', 'calling all cooks', 'cal fire', '21st century farmhouse', 'brittany murphy: an id mystery', 'how close can i beach?', 'supermarket stakeout: what would alex make?', 'the white room challenge', 'mythbusters mini myths', 'homestead rescue: raney ranch', 'did he do it?', 'renovation realities: dale jr. & amy', 'the devils ride', 'ready to love', 'trav', 'ultimate ninja challenge', 'outrageous pumpkins']
series_name= series_name + ["Gordon's Great Escape", 'Gorilla Family And Me', 'Grave Mysteries', 'Grave Secrets', 'Great American Eclipse', 'Great Global Clean Up', 'Great Planes', 'Greece with Simon Reeve', 'Grill It! With Bobby Flay', 'Grill Power', 'Grizzly Bear Cubs and Me', 'Growing Belushi', 'Growing Floret', 'Growing Up Evancho', 'Guardians of the Glades', 'Guiding Alaska', 'Guilty Pleasures', 'Guilty Rich', 'Guns on Campus: Tamron Hall Investigates', 'Gunslingers', 'Guts', 'Guy Off the Hook', "Guy's Big Bite", "Guy's Big Game", "Guy's Big Project", "Guy's Family Road Trip", "Guy's Grocery Games", "Guy's Grocery Games: Guy Cooks the Games", "Guy's Ranch Kitchen", 'Gypsy Sisters', "Gypsy's Revenge", 'Hacking the Wild', 'Hair Goddess', 'Halloween Baking Championship', 'Halloween Wars', 'Ham on the Street', 'Hammered with John & Jimmy DiResta', 'Hands and Feet', 'Handsome Devils', 'Happily Never After', 'Hard to Kill', 'Hardcover Mysteries', 'Harley and the Davidsons', 'Harry & Meghan: A Royal Romance', 'Harvey Weinstein: ID Breaking Now', 'Haunted Case Files', 'Haunted Gingerbread Showdown', 'Haunted Hospitals', 'Haunted LIVE', 'Haunted Towns', 'Haunted USA', 'Haunting in the Heartland', 'Hawaii Hunters', 'Hawaii Life', 'Hayley Ever After: The Dress', 'He Lied About Everything', 'Health Inspectors', 'Healthy Appetite with Ellie Krieger', 'Hear Me, Love Me, See Me', 'Hear No Evil', 'Heart of Darkness', 'Heartbreakers', 'Heat Seekers', 'Heavy Metal Task Force', 'Hell House', "Hell's Kitchen USA", 'Hello World!', 'Helltown', 'Help My Yelp', 'Help! I Wrecked My House', 'Heritage Hunters', 'HGTV Classic- My First Place', 'HGTV Design Star', 'HGTV Dream Home', 'HGTV House Party', 'HGTV Smart Home', 'HGTV Urban Oasis', "HGTV'd", 'Hidden City', 'Hidden Kingdoms', 'Hidden Money Makeover', 'Hidden Potential', 'High School Moms', 'Highway to Hell', 'Highway to Sell', 'Hillbilly Handfishin’', 'History Of Science', 'Hitler', "Hitler's Zombie Army", 'Hoarders', 'Hoarding: Buried Alive', 'Holiday Baking Championship', 'Holiday Cookie Builds', 'Holiday Crafters Gone Wild', 'Holiday Gingerbread Showdown', 'Holiday Wars', 'Holmes and Holmes', 'Holmes: Buy It Right', 'Holmes: Next Generation', 'Home Alone', 'Home for Dinner with Jamie Deen', 'Home Made Simple', 'Home on the Road with Johnnyswim', 'Home Strange Home', 'Home Sweet Homicide', 'Home Town', "Home Town: Ben's Workshop", 'Homegrown', 'Homestead Rescue', 'Homestead Rescue: Raney Ranch', 'Hometown Homicide', 'Hometown Homicide: Local Mysteries', 'Hometown Horror', 'Homicide City', 'Homicide City: Charlotte', 'Honor Flight Heroes', 'Hook, Line & Dinner', 'Horizon: Aftershock - Hunt for Gravitational Waves', 'Horizon: Aftershock- The Hunt for Gravitational Wave', 'Horizon: Antarctica Ice Station Rescue', 'Horizon: Are We Still Evolving?', 'Horizon: Are You Good Or Evil?', 'Horizon: Avalanche - Making a Deadly Snowstorm', 'Horizon: Back From The Dead', 'Horizon: Battle In Your Mind', 'Horizon: Being Transgender', 'Horizon: Body Clock - What Makes Us Tick?', 'Horizon: Clean Eating - The Dirty Truth', 'Horizon: Cyber Attack - The Inside Story', 'Horizon: Dancing in the Dark - The End of Physics?', 'Horizon: Dawn Of The Driverless Car', 'Horizon: Dinosaurs', 'Horizon: How Big Is The Universe?', 'Horizon: How Small Is The Universe?', 'Horizon: How To Build An Astronaut', 'Horizon: Ice Station Antarctica', 'Horizon: Life, Death and Mistakes', 'Horizon: Man On Mars - Mission To The Red Planet', "Horizon: Mars - A Traveller's Guide", 'Horizon: Obsessive Compulsive Disorder', 'Horizon: Oceans Of The Solar System', 'Horizon: Playing God', 'Horizon: Should We Close Our Zoos?', 'Horizon: Should You Really Play Video Games?', 'Horizon: The Core', 'Horizon: The End Of The Solar System', 'Horizon: The Lost Tribes Of Humanity', 'Horizon: The Science Of Laughter', 'Horizon: The Weirdest Weather In The Universe', "Horizon: Tomorrow's World", 'Horizon: What Is Reality?', 'Horizon: What Makes a Psychopath?', 'Horizon: Why Did I Go Mad?', 'Horror At the Cecil Hotel', 'Hostage: Do or Die', 'Hot & Heavy', 'Hot Grease', 'Hot Mess House', 'Hot Properties: San Diego', 'Hotel Amazon', 'Hotel Impossible', 'Hotel Impossible: Showdown', 'Hotel Secrets & Legends', 'Hotel Showdown', "Houdini's Last Secrets", 'House Crashers', 'House Hunters Comedians On Couches: Unfiltered', 'House Hunters Family', 'House Hunters Renovation', 'House Hunters: Comedians on Couches', 'House Hunters: Outside the Box', 'House Hunters: Where Are They Now?', 'House In A Hurry', 'House of Horrors: Kidnapped', 'Houston Beauty', 'How (Not) To Kill Your Husband', 'How Booze Built America', 'How Close Can I Beach?', 'How Do Animals Do That?', 'How Do They Do It?', "How It's Made", "How It's Made: Dream Cars", 'How Nature Works', 'How the Earth Works', 'How the Universe Works', 'How the World Ends', 'How To Build A Planet', 'How To Build... Everything', 'How To Live Longer - The Big Think', 'How We Got Here', 'Hubble: Thirty Years of Discovery', 'Human Journey', 'Hungry Girl', 'Hunting Nazi Treasure', 'I (Almost) Got Away with It', 'I Am Homicide', 'I Am Jazz', "I Didn't Know I Was Pregnant", 'I Escaped: Real Prison Breaks', 'I Found the Gown', 'I Hart Food', 'I Hate My Bath', 'I Hate My Kitchen', 'I Hate My Yard', 'I Kid You Not', "I Love a Mama's Boy", 'I Quit', 'I Should Have Known', 'I Want THAT Wedding', 'I Want That: Builders, Kitchen and Bath Show', 'I Want That: Consumer Electronics Show', 'I Was Murdered', 'I Was Prey', 'I, Witness', "I'd Kill For You", "I'm Pregnant And...", 'Ice Brigade', 'Ice Cold Gold', 'Ice Cold Killers', 'Ice Lake Rebels', 'Ice Road Truckers', 'ID Investigates: Killer Truckers', 'IDCON 2018: Cold Case Confidential', 'Idris Elba: No Limits', 'If I Should Die', 'If Walls Could Talk…', 'If We Built It Today', 'Impact of Hate: Charlottesville', 'Impact of Murder', 'Impossible Croc Rescue', 'Impossible Engineering', 'Impossible Fixes', 'Impostors', 'In Memoriam', 'In Orbit - How Satellites Rule Our World', 'In Plain Sight', 'In Pursuit with John Walsh', 'In Search of Monsters', 'In the Line of Fire', 'In the Pit', 'Incredible Edible America', 'Indecent Proposal', 'Indian Ocean with Simon Reeve', 'Indoors Out', 'Infested!', 'Injustice Files', 'Insane Coaster Wars', 'Insane Coaster Wars: World Domination', 'Insane Pools: Off The Deep End', 'Inseparable: Joined at the Head', "Inside El Chapo's Cartel", 'Inside Secret Societies', "Inside the Vatican's Vault", 'Inspire A Difference', 'Interiors Inc.', 'Intervention', 'Into the Blue Hole', 'Into the Universe with Stephen Hawking', 'Into the Unknown', 'Into The Wild With Gordon Buchanan', 'Intruders', 'Invention Hunters', 'Invisible Killers', 'Invisible Worlds', 'Ireland with Simon Reeve', 'Iron Chef America', 'Iron Chef Gauntlet', 'Iron Chef Showdown', 'Is OJ Innocent? The Missing Evidence', 'Island Explorers', 'Island Hunters', 'Island Life', 'It Feels Evil', 'It Takes a Thief', "It's Me or the Dog", 'Ivory Wars', 'Iyanla: Fix My Life', "Jaguars - Brazil's Super Cats", "James Ellroy's City of Demons", "James Patterson's Murder is Forever", 'Jamie Cooks Italy', 'Jeffrey Dahmer: Mind of a Monster', "Jeremy Wade's Dark Waters", "Jeremy Wade's Mighty Rivers", 'Jesse James: Outlaw Garage', 'Jessica Chambers: An ID Murder Mystery', 'JFK: The Lost Tapes', "Joanna Lumley's Silk Road Adventure", 'Jockeys', 'Jodie Marsh Gets Locked Up', 'Joe Exotic: Before He Was King', 'Joe Exotic: Tigers, Lies and Cover-Up', 'Jon & Kate Plus 8', 'JonBenét Ramsey: What Really Happened?', 'Josh Gates Tonight', 'Journey To Fire Mountain', 'Judgement Day: Prison or Parole', "Judi Dench's Wild Borneo Adventure", 'Jungle Gold', 'Junk Food Flip', 'Junk Gypsies', 'JUNKies', 'Kangaroo Dundee', 'Kaplan America', "Karma's A B*tch!", 'Kate Plus 8', "Kelsey's Essentials", 'Kentucky Murder Mystery: The Trials of Anthony Gray', 'Kid In a Candy Store', 'Kid Tycoons', 'Kidnap and Rescue', 'Kidnapped: Three Days in Hell', 'Kids Baking Championship', 'Kids BBQ Championship', 'Kids Halloween Baking Championship', 'Killer Bods', 'Killer Carnies', 'Killer Clergy', 'Killer Confessions', 'Killer in Question', 'Killer Inspiration', 'Killer Instinct with Chris Hansen', 'Killer Outbreaks', 'Killer Unknown', 'Killer Whales: The Mega Hunt', 'Killing Fields', 'Killing Richard Glossip', 'Killing Time', 'Kindred Spirits', 'King of Dirt', 'Kiss of Death', 'Kitchen Boss', 'Kitchen Casino', 'Kitchen Cousins', 'Kitchen Crashers', 'Kitchen Expedition', 'Kitchen Impossible', 'Kitchen Nightmares USA', 'Kiwi Survival', 'Klondike', 'Kodiak', 'LA Ink', 'Lakefront Bargain Hunt', 'Lakefront Bargain Hunt Renovation', 'Lands Of The Monsoon', 'Las Vegas Law', 'Last American Cowboy', 'Last Cake Standing', 'Last Chance Lawyer', 'Last Days of Pompeii', 'Last Outpost', 'Last Seen Alive', 'Law on the Border', 'League of Monkeys', "Leah Remini: It's All Relative", 'Leah Remini: Scientology And The Aftermath', 'Leave it to Niecy', 'Legend of Croc Gold', 'Legendary Locations', 'Legends of the Deep', 'Legends of the Lost with Megan Fox', 'Legends of the Wild', 'Life', 'Life After: Chernobyl', 'Life Or Death', 'Life Story', "Life's a Beach", 'Little Boy Lost: An ID Mystery', 'Little Giants', 'Little Miss Atlanta', 'Little People, Big World', 'Living a Nightmare', 'Living Abroad', 'Living Alaska', 'Living Big Sky', 'Living with Maneaters', 'Lobstermen', 'Loch Ness Monster: New Evidence', 'Log Cabin Living', 'Lone Star Justice', 'Lone Star Law', 'Lone Target', 'Long Island Medium', 'Long Lost Family', 'Long Lost Family: What Happened Next', 'Lost Beasts of the Ice Age', 'Lost Cities of the Amazon', 'Lost Gold', 'Lost Kingdom of the Black Pharaohs', 'Lost Tapes', 'Lost Women of NXIVM', 'Louisiana Flip N Move', 'Louisiana Lockdown', 'Love & Marriage: Huntsville', 'Love at First Kiss', 'Love at First Swipe', 'Love Goals', 'Love It or List It', 'Love It or List It Australia', 'Love It or List It, Too', 'Love Kills', 'Love the Way You Lie', 'Love Yurts', 'Love, Lust or Run', 'Lovely Bites', 'Lovely Bites by Chef Lovely', 'Lovetown, USA', 'Machines: How They Work', "Macy's Thanksgiving Cake Spectacular", 'Mad Dog Made', 'Madagascar', 'Made By Destruction', 'Made in America', 'Madeleine McCann: An ID Murder Mystery', 'Madman of the Sea', "Mafia's Greatest Hits", 'Magic Man', 'Magnolia Network: A Look Ahead', 'Magnolia Table with Joanna Gaines', 'Mail Order Murder', 'Maine Cabin Masters', 'Making It Home with Kortney and Dave', 'Making Monsters', 'Man Caves', 'Man Fire Food', 'Man Land', 'Man v. Food', 'Man v. Food Nation', 'Man v. Food with Adam Richman', 'Man v. The Universe', 'Man vs. Bear', 'Man vs. Wild', 'Man with a Van', 'Man-Eating Python', 'Man, Cheetah, Wild', 'Man, Woman, Wild', "Man's Greatest Food", 'MANE', 'Manhunt: Kill or Capture', 'Mansions & Murders', 'March to Justice', "Mark & Derek's Excellent Flip", 'Marooned', 'Married At First Sight', 'Married By Mom and Dad', 'Married with Secrets', 'Marrying Millions', 'Martha Knows Best', 'Master of Arms', 'Masters of Flip', 'Meat & Potatoes', 'Mediterranean Life', 'Mediterranean with Simon Reeve', 'Meet The Humans', 'Meet the Putmans', "Meg's Great Rooms", 'Mega Decks', 'Mega Dens', 'Mega Machines', 'Mega Shippers', 'Mega Zoo', "Megastorm: World's Biggest Typhoon", 'Meghan & Harry: A Royal Baby Story', 'Meghan Markle: A Royal Love Story', 'Melting: Last Race to the Pole', 'Memory', 'Men, Women, Wild', 'Mexican Made Easy', 'Mexico Life', 'Miami Flip', 'Miami Ink', 'Michael Jackson: Searching for Neverland', 'Million Dollar Contractor', 'Million Dollar Rooms', 'Misfit Garage', 'Mission Declassified', 'Mission Tomorrow: Your Space Trivia Challenge', 'Modern Sniper', "Mom's Got Game", 'Monkey Planet', 'Monster Bug Wars', 'Monster Favorites', 'Monster Garage', 'Monster Ships', 'Monsters & Mysteries in America', 'Monsters in My Head', 'Monsters Inside Me', 'Monsters Underground', 'Moon Machines', 'Moonshiners', 'Moonshiners: Master Distiller', 'Moonshiners: Whiskey Business', 'Mosquito', 'Most Evil', 'Most Likely To...', 'Most Terrifying Places in America', 'Motives & Murders: Cracking the Case', 'Mountain Life', 'Mountain Men', 'Mountain Monsters', 'Mounted Branch', "Mud Lovin' Rednecks", 'Mummies Unwrapped', 'Mummy Unexplained Files', 'Murder Among Friends', 'Murder By Numbers', 'Murder Calls', 'Murder Chose Me', 'Murder Comes Home', 'Murder Comes To Town', 'Murder Decoded', 'Murder in Amish Country', 'Murder in Paradise', 'Murder in the Heartland', 'Murder in Ypsilanti: Keith Morrison Investigates', 'Murder Loves Company', 'Murder U', 'Mutant Planet', 'My 600-lb Life', 'My 600-lb Life: Where Are They Now?', 'My Big Amazing Renovation', 'My Big Family Renovation', 'My Big Fat American Gypsy Wedding', 'My Big Fat Fabulous Life', 'My Big Italian Adventure', 'My Cat From Hell', 'My Crazy Birth Story', 'My Crazy Obsession', 'My Extreme Animal Phobia', "My Family's Deadly Secret", 'My Favorite Place', 'My Feet Are Killing Me', 'My Feet Are Killing Me: First Steps', 'My First Home', 'My Five Wives', 'My Giant Life', "My Grandmother's Ravioli", 'My Horror Story', "My Kid's Obsession", 'My Lottery Dream Home', 'My Lottery Dream Home International', 'My Murder Story', 'My Pregnant Husband', 'My Strange Addiction', 'My Strange Criminal Addiction', 'My Teen is Pregnant And So Am I', 'My Tiny Terror', 'Mysteries at the Monument', 'Mysteries at the Museum', 'Mysteries of Apollo', 'Mysteries of the Abandoned', 'Mysteries of the Abandoned: Animal Uprising', 'Mysteries of the Deep', 'Mysteries of the Missing', 'Mysteries of the Outdoors']
episode_name = [' Callout Fallout', '0-100 in Under Two Seconds', '1 Brother, 4 Sisters, 2 Rooms', '1 Euro Dream Home: Episode 1', '1 Euro Dream Home: Episode 2', '1 Euro Dream Home: Episode 3', '1 Month Down, Quarantine to Go', '1-800-GUY', '1, 2, 3 Delicious!', '1,000 Pounds to Freedom', '1,000+ New Scientific Samples', '1st + Forever Home', '1st Edition Apparition', '2 Bathrooms, No Bedroom', '2 Chainz, 1 Tank', '2 Dresses, 1 Dream', '2 for 1', '2 Jackets, 4 Dancers', '2 Ladies 4 Pitbulls 1 Baby', '2 Parents, 6 Children, 1 Dog', '2 Wheel Drive', '2-Headed Shark Attack', '2-in-1', '2nd Annual Film Festival Party', '3 a.m. Girls', '3 a.m. Girls: One Year Later', '3 All-American Holiday Homes', '3 Axles and a Baby', '3 Daughters, 1 Dead Son', '3 Design Star Holiday Homes', '3 DIY Fall Scents', "3 DIY Mother's Day Gifts", '3 Funky Holiday Homes', '3 Generations, 1 Big Makeover', '3 Houses, 2 Babies, 1 Decision', '3 Nostalgic Holiday Homes', '3 Sided Square Meal', '3 Weddings and a Robert', '3-2-1 Blast Off!', '3-D Printers and More', '3-Headed Shark Attack', "3-Salad Chef's Salad Plate", '3,559 Miles to a Dream', '3D Signs and Mattresses', '4 Houses, 4 Relationships', '4 Super-Fast Suppers', '4 Under 40', '4 Wives, 4 Valentines', '4 Women and a Funeral', '4-Star Diner', '4-Star Luxury Hotel Suite', '4-Star Salad Bar', '4,000 Square Feet of Trouble', '4th Down and Yum', '4th of July', '4th of July Live', '4th of July Special', '4th Street House', '5 Acres Of Junk', '5 Alarm BBQ', '5 Babies on a Budget', '5 Easy Dinners', '5 Ingredient Fuel', '5 Kids Who Are So Over It', '5 Million Dollar Season', "5 O'clock is Dinnertime", '5 Star CA: Good Dog', '5 Star CT: All for the Honey', '5 Star Hawaii: Wowie Maui', '5 Star NV: Vegas VIP', '5 Star NY: Palace of Spirits', '5 Star WV: Royal Treatment', '5 Star: One and Only Cabo', '5 Star: Wet and Wild Atlantis', '5 Times and No Fun', '5-Day Make Ahead Dinner', '5-Star Adventure in Lisbon', '5-Year Storm, Part 1', '5-Year Storm, Part 2', '5, 10, 15', '5, 10, 15 Part Two', '5,000 Kids and Tickled Pink', '5,000-mile Hunt', '5K Run', '5th Avenue Duplex (Part I)', '5th Avenue Duplex (Part II)', '5th Wheel Mansion', '6 Kids, 5 Baby Daddies', '6 Months Later', '7 Broken Brothers: Part 1', '7 Broken Brothers: Part 2', '7 Broken Brothers: Part 3', "7 Deadly Jack-o'-Lanterns", '7 Deadly Sins', '7 People with 7 Opinions', '7 Ways Kids Show Love', '7th Inning Splits', '8 Babies for Eugene', '8 Landscapes in 8 Hours', '8 Little Johnstons?', '8 Movie Makers', '8-Day Gut Job', '8WD Rescue Vehicle', '9 Miles of Chaos', '9-1-1 Encounters: Beasts in Your Neighborhood', '9-1-1 Encounters: Unleashed, Untamed and Unexplained', '9/11 Firehouse', '9/11: As We Watched', '10 All in the Family Moments', '10 Big Years', '10 Brides Dare to Be Different', '10 Extraordinary Entourages', '10 Kids, No Room, No Problem', '10 Little Pumpkins', '10 Pounds of Gold', '10 Things I Love About Ladd', '10 Year Anniversary', '10 Years and Busier Than Ever!', "10-Minute Beginner's Workout", '10th Anniversary OCC Bike', '10th Anniversary or Bust', '11th Hour', '12 Ingredients All Day', '12 Years a Fugitive', "13 x 9 and Feelin' Fine", '14 and Looking for Mr. Right', '14-Mile House', '15 Days in Hell', '15 Million Dollar Season', '15 Minute Pastas', '15-Minute Dance With Weights', '15-Minute, 150-Calorie Workout', '16 Minute Meals: Italian', '16 Minute Meals: Pasta Pronto', '16 Women, 1 RV', '16-Minute Chicken', '16-Minute Comfort', '16-Minute Dinners', '16-Minute Meals: All Day Long', '16-Minute Meals: Cowboy Style', '16-Minute Meals: On Standby', '16-Minute Meals: Summer', '16-Minute Summertime', '16-Minute Tex Mex', '16-Minute Weeknight Dinners', '16-Pound Tumor', '18, Stupid and Free', '19 Designers and 1 Fanuka', '19th Century Corncrib', '19th-Century Holiday Feast', '19th-century vs. Coliseum', '20 Million Trees by 2020', '20 to 1', '20 Years of Trent and Amber', '20-Foot Terror', '20-Minute Cardio Dance Workout', '20-Minute Dance and Sculpting', '20-Minute Pregnancy Workout', '20th Anniversary at The Opry', '20th-Century Women', '21 Chum Street', '21 Miles, 21 Days', '21-story Free Fall', '21st Century Bathroom', '21st Century Chocolate', '21st Century Farmhouse', '21st Century Renovation', '21st-Century Oil and Gas', '22 Brawling Bridesmaids', '22 Hours of Terror', '22 Year Facelift', '22,000 Foot Fall', '23 Days', '24 Hours of Daytona, Rum', '24 hours on the Job', '24 Hours With Theresa', '24-hour Wedding Challenge', '24/7 Wild', '25 and Counting', '25 Ingredients or Less', '25 Years and Counting', "25-Minute Runner's Recovery", '25th Anniversary', '25th Street Project', '26 Things in Indianapolis', '27 Ton Grill', '28 Foster Homes', '30 Dollar Date', '30 Inches Tall and Turning 18', '30 Minute by Design', '30 Minute Decathalon', '30 Minute Deep Freeze', '30 Minute Dinner Club', '30 Minute Gut Buster', '30 Minute Home Game', '30 Minute Legacy', '30 Minute Personal Day', '30 Minute Renovations', '30 Minute Spaghetti Western']
brand_name = ['(All)', 'Null', 'AEAE', 'AEHI', 'AELF', 'AHC', 'APL', 'BBC', 'COOK', 'DAM', 'DIY', 'DLF', 'DPLUSORIG', 'DSC', 'FOOD', 'GNDO', 'GNNT', 'GNPS', 'GNSK', 'GNTH', 'HGTV', 'IDS', 'MAG', 'OWN', 'SCI', 'TLC', 'TRAV', 'UNB']


# url = urls[0]
input_url = pd .read_csv("ip_urls.csv")
urls = list(input_url['ReportURL'])
urls = urls[11:35]
#get login
result = []
browser = get_login(user_id=okta_user_id,user_passwd=okta_user_passwrd,
                    delay=135)

time.sleep(10)

for url in urls:

    result_dict = init_result_dict()
    result_dict['dashboard_url']= url

    try:
        
        print("Extracting for url:",url)
        browser = get_load_dashbrd(browser,url,
                         delay=130)
        
        print("Extracting Source Html")
        html_source = get_html_dashbrd(browser)

        print("Extracting Source Html")        
        keywrds_dshbrd = get_words_frm_html(html_source)        
        keywrds_dshbrd_clean = text_cleaning(keywrds_dshbrd)
        keywrds_dshbrd_clean  = remove_element(keywrds_dshbrd_clean,noise_text)
        keywrds_dshbrd_clean = [ele for ele in keywrds_dshbrd_clean if '{' not in ele]
        result_dict['WorkBook'] = str([ele for ele in keywrds_dshbrd_clean if 'Workbook' in ele]).replace('Workbook','').replace('[','').replace(']','').replace(':','')
        
        print("Extracting Filter Name")    
        filter_titles = get_filter_name(html_source)#
        
        print("Extracting Filter Values")        
        filter_values = get_filter_value(browser,list(range(len(filter_titles))))

        print("Extracting Parameter Name")    
        parameter_titles = get_parameter_name(html_source)#

        print("Extracting Parameter Filter Values") 
        parameter_values = get_parameter_value(browser,list(range(len(parameter_titles))))


        final=[]
        try:
            
            result_dict['filter_name'] = filter_titles
            result_dict['filter_values'] = filter_values
            result_dict['parameter_name'] = parameter_titles
            result_dict['parameter_values'] = parameter_values
            result_dict['Keywords'] = keywrds_dshbrd_clean


            #Removing Dragdown List as per matching (Series Name,Episode Name):    
            filter_values = drop_match_list(filter_values,series_name,10)        
            filter_values = drop_match_list(filter_values,episode_name,15)        
            filter_values = drop_match_list(filter_values,brand_name,15)
    
            parameter_values = drop_match_list(parameter_values,series_name,15)
            parameter_values = drop_match_list(parameter_values,episode_name,15)
            parameter_values = drop_match_list(parameter_values,brand_name,15)
    
            parameter_values = flatten(parameter_values)
            filter_values = flatten(filter_values)
            # final= filter_titles+filter_values+parameter_titles+parameter_values+keywrds_dshbrd_clean        
            final= filter_titles+filter_values+parameter_titles+parameter_values       
            
            #Removing All Dates
            final = [ele for ele in final if '/' not in ele]
   
            #drop entire element/string
            noise = ['Home','@gmail.com','@discovery.com'
                                       ,'Sort By','select all','show quick filter','yes','no','all',
                                       '(Select A Title Below)','Only Relevant Values','all',
                                       '(all)','(yes)','(no)','x',
                                       'Show Quick Filter Context Menu','(select a title below)',
                                       'All Values In Database','Inclusive','inclusive','exclusive',
                                       'Exclusive','only relevant values','**note ','note'
                                       'dimensions','Jason_Mussman@Discovery.Com','highly confidential - do not share']
            
            
            final = textcleaner(final,noise,
                                match_anywhere=False,
                start_match=True,end_match=False)
 
                        
            final = textcleaner(final,noise,
                                match_anywhere=False,
                start_match=False,end_match=True)
            
            final = textcleaner(final,noise,
                               match_anywhere=True,
               start_match=False,end_match=True)
            
            #Replace Character in element
            final = replace_chars(final,['-','@','#'],any_match=False,startswith=False,
                                  endswith=True)
            # replace_chars(original_list,noise_list,
            #       regex=False,any_match=True,
            #       startswith=True,endswith=True)
            result_dict['final'] = str(final).replace('[','').replace(']','')
            
        except:
            print("unable top get parameters")
        result.append(result_dict)

    except Exception as e:
        print("Error Dashboard: ",url)
        print(e)

result_df = pd.DataFrame(result)
result_df.to_excel('result_df_207_1.xlsx')
browser.close()

# 1,11,17,18 