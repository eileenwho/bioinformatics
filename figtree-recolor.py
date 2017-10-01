#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import re

# These colors are taken from http://www.colorhexa.com/color-names
NAMED_COLORS = {
    'air force blue': '5d8aa8',
    'alice blue': 'f0f8ff',
    'alizarin crimson': 'e32636',
    'almond': 'efdecd',
    'amaranth': 'e52b50',
    'amber': 'ffbf00',
    'american rose': 'ff033e',
    'amethyst': '9966cc',
    'android green': 'a4c639',
    'anti-flash white': 'f2f3f4',
    'antique brass': 'cd9575',
    'antique fuchsia': '915c83',
    'antique white': 'faebd7',
    'ao': '008000',
    'apple green': '8db600',
    'apricot': 'fbceb1',
    'aqua': '00ffff',
    'aquamarine': '7fffd4',
    'army green': '4b5320',
    'arylide yellow': 'e9d66b',
    'ash grey': 'b2beb5',
    'asparagus': '87a96b',
    'atomic tangerine': 'ff9966',
    'auburn': 'a52a2a',
    'aureolin': 'fdee00',
    'aurometalsaurus': '6e7f80',
    'awesome': 'ff2052',
    'azure': '007fff',
    'azure mist/web': 'f0ffff',
    'baby blue': '89cff0',
    'baby blue eyes': 'a1caf1',
    'baby pink': 'f4c2c2',
    'ball blue': '21abcd',
    'banana mania': 'fae7b5',
    'banana yellow': 'ffe135',
    'battleship grey': '848482',
    'bazaar': '98777b',
    'beau blue': 'bcd4e6',
    'beaver': '9f8170',
    'beige': 'f5f5dc',
    'bisque': 'ffe4c4',
    'bistre': '3d2b1f',
    'bittersweet': 'fe6f5e',
    'black': '000000',
    'blanched almond': 'ffebcd',
    'bleu de france': '318ce7',
    'blizzard blue': 'ace5ee',
    'blond': 'faf0be',
    'blue': '0000ff',
    'blue bell': 'a2a2d0',
    'blue gray': '6699cc',
    'blue green': '0d98ba',
    'blue purple': '8a2be2',
    'blue violet': '8a2be2',
    'blush': 'de5d83',
    'bole': '79443b',
    'bondi blue': '0095b6',
    'bone': 'e3dac9',
    'boston university red': 'cc0000',
    'bottle green': '006a4e',
    'boysenberry': '873260',
    'brandeis blue': '0070ff',
    'brass': 'b5a642',
    'brick red': 'cb4154',
    'bright cerulean': '1dacd6',
    'bright green': '66ff00',
    'bright lavender': 'bf94e4',
    'bright maroon': 'c32148',
    'bright pink': 'ff007f',
    'bright turquoise': '08e8de',
    'bright ube': 'd19fe8',
    'brilliant lavender': 'f4bbff',
    'brilliant rose': 'ff55a3',
    'brink pink': 'fb607f',
    'british racing green': '004225',
    'bronze': 'cd7f32',
    'brown': 'a52a2a',
    'bubble gum': 'ffc1cc',
    'bubbles': 'e7feff',
    'buff': 'f0dc82',
    'bulgarian rose': '480607',
    'burgundy': '800020',
    'burlywood': 'deb887',
    'burnt orange': 'cc5500',
    'burnt sienna': 'e97451',
    'burnt umber': '8a3324',
    'byzantine': 'bd33a4',
    'byzantium': '702963',
    'cg blue': '007aa5',
    'cg red': 'e03c31',
    'cadet': '536872',
    'cadet blue': '5f9ea0',
    'cadet grey': '91a3b0',
    'cadmium green': '006b3c',
    'cadmium orange': 'ed872d',
    'cadmium red': 'e30022',
    'cadmium yellow': 'fff600',
    'cafe au lait': 'a67b5b',
    'cafe noir': '4b3621',
    'cal poly pomona green': '1e4d2b',
    'cambridge blue': 'a3c1ad',
    'camel': 'c19a6b',
    'camouflage green': '78866b',
    'canary': 'ffff99',
    'canary yellow': 'ffef00',
    'candy apple red': 'ff0800',
    'candy pink': 'e4717a',
    'capri': '00bfff',
    'caput mortuum': '592720',
    'cardinal': 'c41e3a',
    'caribbean green': '00cc99',
    'carmine': 'ff0040',
    'carmine pink': 'eb4c42',
    'carmine red': 'ff0038',
    'carnation pink': 'ffa6c9',
    'carnelian': 'b31b1b',
    'carolina blue': '99badd',
    'carrot orange': 'ed9121',
    'celadon': 'ace1af',
    'celeste': 'b2ffff',
    'celestial blue': '4997d0',
    'cerise': 'de3163',
    'cerise pink': 'ec3b83',
    'cerulean': '007ba7',
    'cerulean blue': '2a52be',
    'chamoisee': 'a0785a',
    'champagne': 'fad6a5',
    'charcoal': '36454f',
    'chartreuse': '7fff00',
    'cherry': 'de3163',
    'cherry blossom pink': 'ffb7c5',
    'chestnut': 'cd5c5c',
    'chocolate': 'd2691e',
    'chrome yellow': 'ffa700',
    'cinereous': '98817b',
    'cinnabar': 'e34234',
    'cinnamon': 'd2691e',
    'citrine': 'e4d00a',
    'classic rose': 'fbcce7',
    'cobalt': '0047ab',
    'cocoa brown': 'd2691e',
    'coffee': '6f4e37',
    'columbia blue': '9bddff',
    'cool black': '002e63',
    'cool grey': '8c92ac',
    'copper': 'b87333',
    'copper rose': '996666',
    'coquelicot': 'ff3800',
    'coral': 'ff7f50',
    'coral pink': 'f88379',
    'coral red': 'ff4040',
    'cordovan': '893f45',
    'corn': 'fbec5d',
    'cornell red': 'b31b1b',
    'cornflower': '9aceeb',
    'cornflower blue': '6495ed',
    'cornsilk': 'fff8dc',
    'cosmic latte': 'fff8e7',
    'cotton candy': 'ffbcd9',
    'cream': 'fffdd0',
    'crimson': 'dc143c',
    'crimson red': '990000',
    'crimson glory': 'be0032',
    'cyan': '00ffff',
    'daffodil': 'ffff31',
    'dandelion': 'f0e130',
    'dark blue': '00008b',
    'dark brown': '654321',
    'dark byzantium': '5d3954',
    'dark candy apple red': 'a40000',
    'dark cerulean': '08457e',
    'dark chestnut': '986960',
    'dark coral': 'cd5b45',
    'dark cyan': '008b8b',
    'dark electric blue': '536878',
    'dark goldenrod': 'b8860b',
    'dark gray': 'a9a9a9',
    'dark green': '013220',
    'dark jungle green': '1a2421',
    'dark khaki': 'bdb76b',
    'dark lava': '483c32',
    'dark lavender': '734f96',
    'dark magenta': '8b008b',
    'dark midnight blue': '003366',
    'dark olive green': '556b2f',
    'dark orange': 'ff8c00',
    'dark orchid': '9932cc',
    'dark pastel blue': '779ecb',
    'dark pastel green': '03c03c',
    'dark pastel purple': '966fd6',
    'dark pastel red': 'c23b22',
    'dark pink': 'e75480',
    'dark powder blue': '003399',
    'dark raspberry': '872657',
    'dark red': '8b0000',
    'dark salmon': 'e9967a',
    'dark scarlet': '560319',
    'dark sea green': '8fbc8f',
    'dark sienna': '3c1414',
    'dark slate blue': '483d8b',
    'dark slate gray': '2f4f4f',
    'dark spring green': '177245',
    'dark tan': '918151',
    'dark tangerine': 'ffa812',
    'dark taupe': '483c32',
    'dark terra cotta': 'cc4e5c',
    'dark turquoise': '00ced1',
    'dark violet': '9400d3',
    'dartmouth green': '00693e',
    'davy grey': '555555',
    'debian red': 'd70a53',
    'deep carmine': 'a9203e',
    'deep carmine pink': 'ef3038',
    'deep carrot orange': 'e9692c',
    'deep cerise': 'da3287',
    'deep champagne': 'fad6a5',
    'deep chestnut': 'b94e48',
    'deep coffee': '704241',
    'deep fuchsia': 'c154c1',
    'deep jungle green': '004b49',
    'deep lilac': '9955bb',
    'deep magenta': 'cc00cc',
    'deep peach': 'ffcba4',
    'deep pink': 'ff1493',
    'deep saffron': 'ff9933',
    'deep sky blue': '00bfff',
    'denim': '1560bd',
    'desert': 'c19a6b',
    'desert sand': 'edc9af',
    'dim gray': '696969',
    'dodger blue': '1e90ff',
    'dogwood rose': 'd71868',
    'dollar bill': '85bb65',
    'drab': '967117',
    'duke blue': '00009c',
    'earth yellow': 'e1a95f',
    'ecru': 'c2b280',
    'eggplant': '614051',
    'eggshell': 'f0ead6',
    'egyptian blue': '1034a6',
    'electric blue': '7df9ff',
    'electric crimson': 'ff003f',
    'electric cyan': '00ffff',
    'electric green': '00ff00',
    'electric indigo': '6f00ff',
    'electric lavender': 'f4bbff',
    'electric lime': 'ccff00',
    'electric purple': 'bf00ff',
    'electric ultramarine': '3f00ff',
    'electric violet': '8f00ff',
    'electric yellow': 'ffff00',
    'emerald': '50c878',
    'eton blue': '96c8a2',
    'fallow': 'c19a6b',
    'falu red': '801818',
    'famous': 'ff00ff',
    'fandango': 'b53389',
    'fashion fuchsia': 'f400a1',
    'fawn': 'e5aa70',
    'feldgrau': '4d5d53',
    'fern': '71bc78',
    'fern green': '4f7942',
    'ferrari red': 'ff2800',
    'field drab': '6c541e',
    'fire engine red': 'ce2029',
    'firebrick': 'b22222',
    'flame': 'e25822',
    'flamingo pink': 'fc8eac',
    'flavescent': 'f7e98e',
    'flax': 'eedc82',
    'floral white': 'fffaf0',
    'fluorescent orange': 'ffbf00',
    'fluorescent pink': 'ff1493',
    'fluorescent yellow': 'ccff00',
    'folly': 'ff004f',
    'forest green': '228b22',
    'french beige': 'a67b5b',
    'french blue': '0072bb',
    'french lilac': '86608e',
    'french rose': 'f64a8a',
    'fuchsia': 'ff00ff',
    'fuchsia pink': 'ff77ff',
    'fulvous': 'e48400',
    'fuzzy wuzzy': 'cc6666',
    'gainsboro': 'dcdcdc',
    'gamboge': 'e49b0f',
    'ghost white': 'f8f8ff',
    'ginger': 'b06500',
    'glaucous': '6082b6',
    'glitter': 'e6e8fa',
    'gold': 'ffd700',
    'golden brown': '996515',
    'golden poppy': 'fcc200',
    'golden yellow': 'ffdf00',
    'goldenrod': 'daa520',
    'granny smith apple': 'a8e4a0',
    'gray': '808080',
    'gray asparagus': '465945',
    'green': '00ff00',
    'green blue': '1164b4',
    'green yellow': 'adff2f',
    'grullo': 'a99a86',
    'guppie green': '00ff7f',
    'halaya ube': '663854',
    'han blue': '446ccf',
    'han purple': '5218fa',
    'hansa yellow': 'e9d66b',
    'harlequin': '3fff00',
    'harvard crimson': 'c90016',
    'harvest gold': 'da9100',
    'heart gold': '808000',
    'heliotrope': 'df73ff',
    'hollywood cerise': 'f400a1',
    'honeydew': 'f0fff0',
    'hooker green': '49796b',
    'hot magenta': 'ff1dce',
    'hot pink': 'ff69b4',
    'hunter green': '355e3b',
    'icterine': 'fcf75e',
    'inchworm': 'b2ec5d',
    'india green': '138808',
    'indian red': 'cd5c5c',
    'indian yellow': 'e3a857',
    'indigo': '4b0082',
    'international klein blue': '002fa7',
    'international orange': 'ff4f00',
    'iris': '5a4fcf',
    'isabelline': 'f4f0ec',
    'islamic green': '009000',
    'ivory': 'fffff0',
    'jade': '00a86b',
    'jasmine': 'f8de7e',
    'jasper': 'd73b3e',
    'jazzberry jam': 'a50b5e',
    'jonquil': 'fada5e',
    'june bud': 'bdda57',
    'jungle green': '29ab87',
    'ku crimson': 'e8000d',
    'kelly green': '4cbb17',
    'khaki': 'c3b091',
    'la salle green': '087830',
    'languid lavender': 'd6cadd',
    'lapis lazuli': '26619c',
    'laser lemon': 'fefe22',
    'laurel green': 'a9ba9d',
    'lava': 'cf1020',
    'lavender': 'e6e6fa',
    'lavender blue': 'ccccff',
    'lavender blush': 'fff0f5',
    'lavender gray': 'c4c3d0',
    'lavender indigo': '9457eb',
    'lavender magenta': 'ee82ee',
    'lavender mist': 'e6e6fa',
    'lavender pink': 'fbaed2',
    'lavender purple': '967bb6',
    'lavender rose': 'fba0e3',
    'lawn green': '7cfc00',
    'lemon': 'fff700',
    'lemon yellow': 'fff44f',
    'lemon chiffon': 'fffacd',
    'lemon lime': 'bfff00',
    'light crimson': 'f56991',
    'light thulian pink': 'e68fac',
    'light apricot': 'fdd5b1',
    'light blue': 'add8e6',
    'light brown': 'b5651d',
    'light carmine pink': 'e66771',
    'light coral': 'f08080',
    'light cornflower blue': '93ccea',
    'light cyan': 'e0ffff',
    'light fuchsia pink': 'f984ef',
    'light goldenrod yellow': 'fafad2',
    'light gray': 'd3d3d3',
    'light green': '90ee90',
    'light khaki': 'f0e68c',
    'light pastel purple': 'b19cd9',
    'light pink': 'ffb6c1',
    'light salmon': 'ffa07a',
    'light salmon pink': 'ff9999',
    'light sea green': '20b2aa',
    'light sky blue': '87cefa',
    'light slate gray': '778899',
    'light taupe': 'b38b6d',
    'light yellow': 'ffffed',
    'lilac': 'c8a2c8',
    'lime': 'bfff00',
    'lime green': '32cd32',
    'lincoln green': '195905',
    'linen': 'faf0e6',
    'lion': 'c19a6b',
    'liver': '534b4f',
    'lust': 'e62020',
    'msu green': '18453b',
    'macaroni and cheese': 'ffbd88',
    'magenta': 'ff00ff',
    'magic mint': 'aaf0d1',
    'magnolia': 'f8f4ff',
    'mahogany': 'c04000',
    'maize': 'fbec5d',
    'majorelle blue': '6050dc',
    'malachite': '0bda51',
    'manatee': '979aaa',
    'mango tango': 'ff8243',
    'mantis': '74c365',
    'maroon': '800000',
    'mauve': 'e0b0ff',
    'mauve taupe': '915f6d',
    'mauvelous': 'ef98aa',
    'maya blue': '73c2fb',
    'meat brown': 'e5b73b',
    'medium persian blue': '0067a5',
    'medium aquamarine': '66ddaa',
    'medium blue': '0000cd',
    'medium candy apple red': 'e2062c',
    'medium carmine': 'af4035',
    'medium champagne': 'f3e5ab',
    'medium electric blue': '035096',
    'medium jungle green': '1c352d',
    'medium lavender magenta': 'dda0dd',
    'medium orchid': 'ba55d3',
    'medium purple': '9370db',
    'medium red violet': 'bb3385',
    'medium sea green': '3cb371',
    'medium slate blue': '7b68ee',
    'medium spring bud': 'c9dc87',
    'medium spring green': '00fa9a',
    'medium taupe': '674c47',
    'medium teal blue': '0054b4',
    'medium turquoise': '48d1cc',
    'medium violet red': 'c71585',
    'melon': 'fdbcb4',
    'midnight blue': '191970',
    'midnight green': '004953',
    'mikado yellow': 'ffc40c',
    'mint': '3eb489',
    'mint cream': 'f5fffa',
    'mint green': '98ff98',
    'misty rose': 'ffe4e1',
    'moccasin': 'faebd7',
    'mode beige': '967117',
    'moonstone blue': '73a9c2',
    'mordant red 19': 'ae0c00',
    'moss green': 'addfad',
    'mountain meadow': '30ba8f',
    'mountbatten pink': '997a8d',
    'mulberry': 'c54b8c',
    'munsell': 'f2f3f4',
    'mustard': 'ffdb58',
    'myrtle': '21421e',
    'nadeshiko pink': 'f6adc6',
    'napier green': '2a8000',
    'naples yellow': 'fada5e',
    'navajo white': 'ffdead',
    'navy blue': '000080',
    'neon carrot': 'ffa343',
    'neon fuchsia': 'fe59c2',
    'neon green': '39ff14',
    'non-photo blue': 'a4dded',
    'north texas green': '059033',
    'ocean boat blue': '0077be',
    'ochre': 'cc7722',
    'office green': '008000',
    'old gold': 'cfb53b',
    'old lace': 'fdf5e6',
    'old lavender': '796878',
    'old mauve': '673147',
    'old rose': 'c08081',
    'olive': '808000',
    'olive drab': '6b8e23',
    'olive green': 'bab86c',
    'olivine': '9ab973',
    'onyx': '0f0f0f',
    'opera mauve': 'b784a7',
    'orange': 'ffa500',
    'orange yellow': 'f8d568',
    'orange peel': 'ff9f00',
    'orange red': 'ff4500',
    'orchid': 'da70d6',
    'otter brown': '654321',
    'outer space': '414a4c',
    'outrageous orange': 'ff6e4a',
    'oxford blue': '002147',
    'pacific blue': '1ca9c9',
    'pakistan green': '006600',
    'palatinate blue': '273be2',
    'palatinate purple': '682860',
    'pale aqua': 'bcd4e6',
    'pale blue': 'afeeee',
    'pale brown': '987654',
    'pale carmine': 'af4035',
    'pale cerulean': '9bc4e2',
    'pale chestnut': 'ddadaf',
    'pale copper': 'da8a67',
    'pale cornflower blue': 'abcdef',
    'pale gold': 'e6be8a',
    'pale goldenrod': 'eee8aa',
    'pale green': '98fb98',
    'pale lavender': 'dcd0ff',
    'pale magenta': 'f984e5',
    'pale pink': 'fadadd',
    'pale plum': 'dda0dd',
    'pale red violet': 'db7093',
    'pale robin egg blue': '96ded1',
    'pale silver': 'c9c0bb',
    'pale spring bud': 'ecebbd',
    'pale taupe': 'bc987e',
    'pale violet red': 'db7093',
    'pansy purple': '78184a',
    'papaya whip': 'ffefd5',
    'paris green': '50c878',
    'pastel blue': 'aec6cf',
    'pastel brown': '836953',
    'pastel gray': 'cfcfc4',
    'pastel green': '77dd77',
    'pastel magenta': 'f49ac2',
    'pastel orange': 'ffb347',
    'pastel pink': 'ffd1dc',
    'pastel purple': 'b39eb5',
    'pastel red': 'ff6961',
    'pastel violet': 'cb99c9',
    'pastel yellow': 'fdfd96',
    'patriarch': '800080',
    'payne grey': '536878',
    'peach': 'ffe5b4',
    'peach puff': 'ffdab9',
    'peach yellow': 'fadfad',
    'pear': 'd1e231',
    'pearl': 'eae0c8',
    'pearl aqua': '88d8c0',
    'peridot': 'e6e200',
    'periwinkle': 'ccccff',
    'persian blue': '1c39bb',
    'persian indigo': '32127a',
    'persian orange': 'd99058',
    'persian pink': 'f77fbe',
    'persian plum': '701c1c',
    'persian red': 'cc3333',
    'persian rose': 'fe28a2',
    'phlox': 'df00ff',
    'phthalo blue': '000f89',
    'phthalo green': '123524',
    'piggy pink': 'fddde6',
    'pine green': '01796f',
    'pink': 'ffc0cb',
    'pink flamingo': 'fc74fd',
    'pink sherbet': 'f78fa7',
    'pink pearl': 'e7accf',
    'pistachio': '93c572',
    'platinum': 'e5e4e2',
    'plum': 'dda0dd',
    'portland orange': 'ff5a36',
    'powder blue': 'b0e0e6',
    'princeton orange': 'ff8f00',
    'prussian blue': '003153',
    'psychedelic purple': 'df00ff',
    'puce': 'cc8899',
    'pumpkin': 'ff7518',
    'purple': '800080',
    'purple heart': '69359c',
    'purple mountain\'s majesty': '9d81ba',
    'purple mountain majesty': '9678b6',
    'purple pizzazz': 'fe4eda',
    'purple taupe': '50404d',
    'rackley': '5d8aa8',
    'radical red': 'ff355e',
    'raspberry': 'e30b5d',
    'raspberry glace': '915f6d',
    'raspberry pink': 'e25098',
    'raspberry rose': 'b3446c',
    'raw sienna': 'd68a59',
    'razzle dazzle rose': 'ff33cc',
    'razzmatazz': 'e3256b',
    'red': 'ff0000',
    'red orange': 'ff5349',
    'red brown': 'a52a2a',
    'red violet': 'c71585',
    'rich black': '004040',
    'rich carmine': 'd70040',
    'rich electric blue': '0892d0',
    'rich lilac': 'b666d2',
    'rich maroon': 'b03060',
    'rifle green': '414833',
    'robin\'s egg blue': '1fcecb',
    'rose': 'ff007f',
    'rose bonbon': 'f9429e',
    'rose ebony': '674846',
    'rose gold': 'b76e79',
    'rose madder': 'e32636',
    'rose pink': 'ff66cc',
    'rose quartz': 'aa98a9',
    'rose taupe': '905d5d',
    'rose vale': 'ab4e52',
    'rosewood': '65000b',
    'rosso corsa': 'd40000',
    'rosy brown': 'bc8f8f',
    'royal azure': '0038a8',
    'royal blue': '4169e1',
    'royal fuchsia': 'ca2c92',
    'royal purple': '7851a9',
    'ruby': 'e0115f',
    'ruddy': 'ff0028',
    'ruddy brown': 'bb6528',
    'ruddy pink': 'e18e96',
    'rufous': 'a81c07',
    'russet': '80461b',
    'rust': 'b7410e',
    'sacramento state green': '00563f',
    'saddle brown': '8b4513',
    'safety orange': 'ff6700',
    'saffron': 'f4c430',
    'saint patrick blue': '23297a',
    'salmon': 'ff8c69',
    'salmon pink': 'ff91a4',
    'sand': 'c2b280',
    'sand dune': '967117',
    'sandstorm': 'ecd540',
    'sandy brown': 'f4a460',
    'sandy taupe': '967117',
    'sap green': '507d2a',
    'sapphire': '0f52ba',
    'satin sheen gold': 'cba135',
    'scarlet': 'ff2400',
    'school bus yellow': 'ffd800',
    'screamin green': '76ff7a',
    'sea blue': '006994',
    'sea green': '2e8b57',
    'seal brown': '321414',
    'seashell': 'fff5ee',
    'selective yellow': 'ffba00',
    'sepia': '704214',
    'shadow': '8a795d',
    'shamrock': '45cea2',
    'shamrock green': '009e60',
    'shocking pink': 'fc0fc0',
    'sienna': '882d17',
    'silver': 'c0c0c0',
    'sinopia': 'cb410b',
    'skobeloff': '007474',
    'sky blue': '87ceeb',
    'sky magenta': 'cf71af',
    'slate blue': '6a5acd',
    'slate gray': '708090',
    'smalt': '003399',
    'smokey topaz': '933d41',
    'smoky black': '100c08',
    'snow': 'fffafa',
    'spiro disco ball': '0fc0fc',
    'spring bud': 'a7fc00',
    'spring green': '00ff7f',
    'steel blue': '4682b4',
    'stil de grain yellow': 'fada5e',
    'stizza': '990000',
    'stormcloud': '008080',
    'straw': 'e4d96f',
    'sunglow': 'ffcc33',
    'sunset': 'fad6a5',
    'sunset orange': 'fd5e53',
    'tan': 'd2b48c',
    'tangelo': 'f94d00',
    'tangerine': 'f28500',
    'tangerine yellow': 'ffcc00',
    'taupe': '483c32',
    'taupe gray': '8b8589',
    'tawny': 'cd5700',
    'tea green': 'd0f0c0',
    'tea rose': 'f4c2c2',
    'teal': '008080',
    'teal blue': '367588',
    'teal green': '006d5b',
    'terra cotta': 'e2725b',
    'thistle': 'd8bfd8',
    'thulian pink': 'de6fa1',
    'tickle me pink': 'fc89ac',
    'tiffany blue': '0abab5',
    'tiger eye': 'e08d3c',
    'timberwolf': 'dbd7d2',
    'titanium yellow': 'eee600',
    'tomato': 'ff6347',
    'toolbox': '746cc0',
    'topaz': 'ffc87c',
    'tractor red': 'fd0e35',
    'trolley grey': '808080',
    'tropical rain forest': '00755e',
    'true blue': '0073cf',
    'tufts blue': '417dc1',
    'tumbleweed': 'deaa88',
    'turkish rose': 'b57281',
    'turquoise': '30d5c8',
    'turquoise blue': '00ffef',
    'turquoise green': 'a0d6b4',
    'tuscan red': '66424d',
    'twilight lavender': '8a496b',
    'tyrian purple': '66023c',
    'ua blue': '0033aa',
    'ua red': 'd9004c',
    'ucla blue': '536895',
    'ucla gold': 'ffb300',
    'ufo green': '3cd070',
    'up forest green': '014421',
    'up maroon': '7b1113',
    'usc cardinal': '990000',
    'usc gold': 'ffcc00',
    'ube': '8878c3',
    'ultra pink': 'ff6fff',
    'ultramarine': '120a8f',
    'ultramarine blue': '4166f5',
    'umber': '635147',
    'united nations blue': '5b92e5',
    'university of california gold': 'b78727',
    'unmellow yellow': 'ffff66',
    'upsdell red': 'ae2029',
    'urobilin': 'e1ad21',
    'utah crimson': 'd3003f',
    'vanilla': 'f3e5ab',
    'vegas gold': 'c5b358',
    'venetian red': 'c80815',
    'verdigris': '43b3ae',
    'vermilion': 'e34234',
    'veronica': 'a020f0',
    'violet': 'ee82ee',
    'violet blue': '324ab2',
    'violet red': 'f75394',
    'viridian': '40826d',
    'vivid auburn': '922724',
    'vivid burgundy': '9f1d35',
    'vivid cerise': 'da1d81',
    'vivid tangerine': 'ffa089',
    'vivid violet': '9f00ff',
    'warm black': '004242',
    'waterspout': '00ffff',
    'wenge': '645452',
    'wheat': 'f5deb3',
    'white': 'ffffff',
    'white smoke': 'f5f5f5',
    'wild strawberry': 'ff43a4',
    'wild watermelon': 'fc6c85',
    'wild blue yonder': 'a2add0',
    'wine': '722f37',
    'wisteria': 'c9a0dc',
    'xanadu': '738678',
    'yale blue': '0f4d92',
    'yellow': 'ffff00',
    'yellow orange': 'ffae42',
    'yellow green': '9acd32',
    'zaffre': '0014a8',
    'zinnwaldite brown': '2c1608',
}


class StringLookup():
    """
    Read string taxa names and their associated colors and provide a find
    method for looking up taxa.
    """
    def __init__(self, fp, matchCase):
        colors = {}
        self.matchCase = matchCase
        # Blank lines and those whose first non-blank character is # are
        # taken to be comments.
        ignoreRe = re.compile('^\s*(?:#.*)?$')

        for line in fp:
            if ignoreRe.search(line):
                continue
            line = line[:-1]
            try:
                taxon, color = line.split(maxsplit=1)
            except TypeError:
                # Python 2
                taxon, color = line.split(None, 1)
            if not color.startswith('#'):
                try:
                    hex6 = NAMED_COLORS[color.lower()]
                except KeyError:
                    raise ValueError('Unrecognized color name %r' % color)
                else:
                    color = '#' + hex6

            if not matchCase:
                taxon = taxon.lower()

            if taxon in colors:
                # We could allow repeats if the color is the same, but a
                # repeated taxon is probably a sign of error.
                raise ValueError('Taxon %r repeated in color file' % taxon)
            colors[taxon] = color

        self.colors = colors

    def find(self, taxon):
        try:
            return self.colors[taxon if self.matchCase else taxon.lower()]
        except KeyError:
            return


class RegexLookup():
    """
    Read regex patterns of taxa names and their associated colors and provide a
    find method for looking up taxa.
    """
    def __init__(self, fp, matchCase):
        regexps = []
        regexpsSeen = set()
        flags = re.UNICODE if matchCase else (re.IGNORECASE | re.UNICODE)
        # Blank lines and those whose first non-blank character is # are
        # taken to be comments.
        ignoreRe = re.compile('^\s*(?:#.*)?$')

        for line in fp:
            if ignoreRe.search(line):
                continue
            line = line[:-1]

            try:
                taxonRegex, color = line.split(maxsplit=1)
            except TypeError:
                # Python 2
                taxonRegex, color = line.split(None, 1)
            if not color.startswith('#'):
                try:
                    hex6 = NAMED_COLORS[color.lower()]
                except KeyError:
                    raise ValueError('Unrecognized color name %r' % color)
                else:
                    color = '#' + hex6

            if taxonRegex in regexpsSeen:
                # We could allow repeated regexps if the color is the same, but
                # a repeated regexp is probably a sign of error.
                raise ValueError('Taxon regex %r repeated in color file' %
                                 taxonRegex)

            regexpsSeen.add(taxonRegex)
            regexps.append((re.compile(taxonRegex, flags), color))

        self.regexps = regexps

    def find(self, taxon):
        # Note: first matching regex wins.
        for regexp, color in self.regexps:
            if regexp.search(taxon):
                return color


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=('Re-color a FigTree NEXUS file.'))


parser.add_argument(
    '--nexusFile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
    help=('The NEXUS file to re-color. If not provided, the Nexus will be '
          'read from standard input.'))

# A mutually exclusive group for either --colorFile or --listColors
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    '--listColors', '--listColours', default=False, action='store_true',
    help=('If specified, all known color names will be printed, after which '
          'the program will exit.'))

group.add_argument(
    '--colorFile', '--colourFile', type=open,
    help=('Give the name of the color file to use. This is a text file '
          'whose lines each have a taxon name, some whitespace, then a '
          'color name. Colors must have 6 RGB hex values, '
          'optionally with a preceeding hash. E.g., DA195 #FF0000'))

parser.add_argument(
    '--defaultColor', '--defaultColour',
    help=('Give a default color. If not specified, nodes will be output with '
          'no color information. May be specified as a 6-digit hex value '
          '(with or without leading #) or as a color name.'))

parser.add_argument(
    '--preserveOriginalColors', '--preserveOriginalColours', default=False,
    action='store_true',
    help=('If specified, taxa that already have a color in the Nexus file, '
          'and which do not appear in the color file, will be printed with '
          'their original color.'))

parser.add_argument(
    '--regex', default=False, action='store_true',
    help=('If specified, taxa names in the color specification file will '
          'be treated as regular expressions.'))

parser.add_argument(
    '--matchCase', default=False, action='store_true',
    help=('If specified, the regular expressions for taxa names in the color '
          'specification file will consider case important in matching in '
          'taxa names.'))


args = parser.parse_args()

if args.listColors:
    maxLen = max(map(len, NAMED_COLORS))
    print('\n'.join(sorted('%-*s #%s' % (maxLen, color, hex6)
                           for (color, hex6) in NAMED_COLORS.items())))
    sys.exit(0)

if args.defaultColor:
    try:
        defaultColor = NAMED_COLORS[args.defaultColor.lower()]
    except KeyError:
        if args.defaultColor.startswith('#'):
            defaultColor = args.defaultColor[1:]
        else:
            defaultColor = args.defaultColor

        # Should check here that this is a hex-string, not an unknown or
        # misspelled color, like browne. But, live dangerously!
        if len(defaultColor) != 6:
            raise ValueError('Unrecognized or incorrect length default '
                             'color: %r' % args.defaultColor)
else:
    defaultColor = None

# Depending on whether the color specification file has taxa as plain
# strings (the default) or as regular expressions, create something we can
# use to look up colors for taxa.
if args.regex:
    lookupTaxon = RegexLookup(args.colorFile, args.matchCase).find
else:
    lookupTaxon = StringLookup(args.colorFile, args.matchCase).find


# A regex to match taxa names in the pre-existing Nexus file.
taxonRe = re.compile("""
                     (\s*) # Optional leading whitespace.
                     (?:
                         '([^']+?)_ # A taxon name preceded by a single quote and followed by a _, nongreedy to only get first bit
                         | #or
                         ([^[]+)\| # A taxon name followed by a |.
                         # |  #or
                         # '([^']+)' # A taxon name in single quotes,
                         # |         # or
                         # ([^[]+)\[ # a taxon name followed by a [.
                         # |         # or
                         # (\w+) # An unadorned taxon name.

                     )
                     """, re.X)
#added line to the end of taxonRe thing

taxaVerbatimRe = re.compile('^\s*(dimensions\s+ntax=\d+;|taxlabels)\s*$')
startOfTaxaRe = re.compile('^\s*begin\s+taxa\s*;\s*$')
endOfTaxaRe = re.compile('^\s*;\s*$')

waitingForTaxaBlock = True
inTaxaBlock = False

# Poor man's line-by-line Nexus parsing, looking for the taxa block.
for line in args.nexusFile:
    if waitingForTaxaBlock:
        if startOfTaxaRe.search(line):
            waitingForTaxaBlock = False
            inTaxaBlock = True
        print(line, end='')
    elif inTaxaBlock:
        if endOfTaxaRe.search(line):
            inTaxaBlock = False
            print(line, end='')
        elif taxaVerbatimRe.search(line): #ok this i don't get
            print(line, end='')
        else:
            match = taxonRe.match(line)
            if match:
                whitespace = match.group(1)
                taxon = match.group(2) or match.group(3) or match.group(4) or match.group(5)
            # rewrite match and rewrite this to just repeat the line with color at the end
            # inLine = taxonRe.search(line)
            # if inLine:
            #     taxon=taxonRe #ah so taxon is this match object thing
                #so lookup needs to be written another way probably
                #need to make this parse the entire line and figure out what the genus is?
            #also maybe i could just rewrite the nexus file so that the taxa are actually the genus
                color = lookupTaxon(taxon)
                if color:
                    line_fix = line.split()[0]
                    color=color.rstrip()
                    print('%s%s[&!color=%s]' % (whitespace, line_fix, color)) #yeah here we want line because nexus includes 'taxon' and also we're looking for taxon within entire line that gets picked up because of underscores and no spaces
                #oh no line includes whitespaces and things
                else:
                    line_fix=line.split("\'")[1]
                    # We have no color for this taxon. Either leave it
                    # alone (i.e., print the original color (if any) or
                    # make sure it is stripped of a color.
                    if args.preserveOriginalColors:
                        print(line, end='')
                    else:
                        if defaultColor:
                            print('%s%s[&!color=#%s]' % (whitespace, line_fix,
                                                         defaultColor))
                        else:
                            print('%s\'%s\'' % (whitespace, line_fix))
            else:
                print(line, end='')
    else:
        print(line, end='')
