# -*- coding:utf-8 -*- 
#!/usr/bin/env python

import random as rnd
import string
import pandas as pd


def generate_name(size, chars = string.ascii_letters + string.digits):
    return ''.join(rnd.choice(chars) for _ in range(size))

def generate_recipe_names(n):
    names = set()
    while len(names) != n: 
        names.add(generate_name(rnd.randint(6, 20)))
    return list(names)

def generate_recipes(n_recipe, ingredients, minimum_amount_of_ingredients, maximum_amount_of_ingredients):
    r = dict()
    for name in generate_recipe_names(n_recipe):
        n = rnd.randint(minimum_amount_of_ingredients, maximum_amount_of_ingredients)
        r[name] = list(set(rnd.choices(ingredients, k=n)))
        
    return r

ingredients = ['huevos','tomate','ajo','leche','arroz','mantequilla','patata','azúcar','zanahoria','orégano','espaguetis','limón','mayonesa','canela','pan','vinagre','manzana','plátano','mostaza','miel','perejil','tortillas','crema','lenteja','vainilla','comino','lechuga','frijoles','cilantro','puerro','calabacín','albahaca','espinaca','apio','berenjena','cebollino','romero','calabaza','pepino','espárrago','brócoli','alcachofa','chalota','coliflor','repollo','eneldo','rúcula','remolacha','elote','acelga','batata','endivia','rábano','tomatillo','hinojo','nabo','boniato','berro','canónigo','yuca','kale','ajete','chayote','jícama','palmito','alfalfa','cardo','chirivía','auyama','cogollos','grelos','calçots','verdolaga','berza','achicoria','borraja','chuño','huacatay','romanescu','romeritos','mandioca','chucrut','acedera','colinabo','olluco','okra','champiñones','trufa','shiitake','portobello','boletus','níscalos','huitlacoche','gírgolas','rebozuelos','crimini','porcini','colmenillas','llanegas','enoki','negrillas','senderuelas','moixernons','shimeji','naranja','aguacate','fresas','piña','mango','lima','frambuesa','pera','arándanos','uva','melocotón','cereza','dátil','kiwi','melón','mandarina','zarzamora','sandía','coco','castaña','granada','ciruela','nopal','pomelo','papaya','albaricoque','membrillo','guayaba','maracuyá','grosella','tamarindo','nectarina','caqui','chabacano','mamey','guanábana','ruibarbo','níspero','tejocote','brevas','kumquat','carambola','chirimoya','lychee','lúcuma','quinotos','lulo','physalis','pitahaya','paraguayo','madroño','açai','pitaya','aguaymanto','curuba','limoncillo','cocona','tamarillo','chontaduro','nance','acerola','guarana','capulín','almendra','nuez','piñones','avellana','cacahuete','pistacho','anacardos','orejón','pacana','macadamia','halva','cheddar','parmesano','mozzarella','ricotta','emmental','gruyere','quesitos','gouda','brie','camembert','havarti','edam','fontina','burrata','cuartirolo','reggianito','petit-suisse','halloumi','provoleta','appenzeller','comté','asiago','sbrinz','arzúa-ulloa','babybel','paneer','taleggio','velveeta','nata','yogur','buttermilk','jocoque','kéfir','cuajo','albúmina','tofu','agar-agar','seitan','algas','tempeh','espirulina','maca','aquafaba','cochayuyo','yuba','tocino','chorizo','panceta','salchicha','sobrasada','butifarra','cecina','longaniza','chistorras','salami','lacón','pepperoni','mortadela','prosciutto','salchichón','charqui','bresaola','coppa','fuet','cuy','pastrami','chalona','speck','conejo','morcilla','chicharrones','caracoles','lenguas','cabrito','tripas','matambre','cochinillo','liebre','ciervo','jabalí','tuétano','lechón','venado','capón','picaña','chilorio','chinchulines','codorniz','perdiz','picantones','pichón','faisán','paloma','oca','ganso','bacalao','salmón','merluza','rape','lubina','lenguado','trucha','mero','boquerón','caballa','besugo','rodaballo','corvina','cazón','tilapia','salmonete','pescadilla','congrio','huachinango','abadejo','jurel','panga','cabracho','raya','palometa','emperador','arenques','pejerrey','perca','pargo','mojarra','bagre','anguila','melva','bacaladilla','morralla','brótola','sargo','surubí','pámpano','pacú','carpa','fogonero','skrei','cabrilla','pageles','tollo','esturión','lamprea','mújol','tenca','acedías','cherna','turbot','barbero','boquinete','alfonsino','cachamas','skipjack','anchoas','sardinas','caviar','angulas','sardella','gamba','langostino','almeja','mejillones','camarón','calamar','pulpo','sepia','surimi','vieira','chipirón','berberecho','cigala','bogavante','langosta','ostras','carabinero','ostión','navaja','centollo','zamburiña','nécora','galera','centolla','percebe','bígaro','quisquilla','abulón','cañaíllas','picorocos','paprika','tomillo','menta','azafrán','clavo','curry','cúrcuma','anís','hierbabuena','cardamomo','epazote','salvia','estragón','achiote','mejorana','culantro','alcaravea','ajinomoto','macis','cajún','enebro','gomasio','algarroba',"za'atar",'zumaque','fenogreco','galangal','melisa','limonaria','poleo','furikake','guascas','eucalipto','agracejo','stevia','panela','melaza','glucosa','granadina','sucralosa','sacarina','xilitol','fructosa','eritritol','acitrón','glicerina','aguamiel','dextrosa','isomalt','sukrin','algarrobina','almáciga','chile','guindilla','cayena','jalapeño','guajillo','ñora','habanero','morita','piquín','peperoncino','panca','cuaresmeño','güero','rocoto','cascabel','shichimi','merquén','cubanela','anaheim','chombo','chiltepin','xcatic','chiltepe','simojovel','chamborote','chirelito','cobán','xiure','maicena','sémola','sprinkles','panko','fondant','xantana','gasificante','tapioca','salvado','merengue','mazapán','pectina','pudín','gofio','vainillin','natafix','arrurruz','manzanilla','pensamientos','violeta','hibisco','lúpulo','jazmín','caléndula','oxalis','sauco','crisantemo','hojaldre','filo','copetín','sésamo','quinoa','chía','cuscús','cereales','amaranto','polenta','granola','bulgur','mijo','semolín','muesli','chufa','psyllium','centeno','pinole','moringa','huauzontle','kiwicha','nigella','amapola','teff','sorgo','airampo','kamut','guisantes','garbanzo','habas','soja','tirabeques','edamame','vainitas','caraotas','garrofón','guandules','pallares','cargamanto','mungo','tallarines','canelones','noodles','ñoquis','soba','orzo','ramen','udon','baguette','picatostes','tartaletas','obleas','chapata','magdalenas','crepes','brioche','panqueques','croissant','pretzel','muffin','focaccia','arepas','waffles','panettone','blinis','matzo','casabe','jalá','margarina','ghee','balsámico','ketchup','wasabi','miso','alioli','bovril','sriracha','tamari','harissa','hogao','katsuobushi','tajín','umeboshi','gochujang','aminos','shoyu','tampico','maíz','alcaparras','kimchi','pickles','altramuces','sauerkraut','tahini','pesto','guacamole','hummus','olivada','chancaca','mojo','salmorreta','gravy','dashi','cocochas','salmorejo','mermelada','calabazate','chocolate','galletas','nutella','turrón','soletilla','malvavisco','natillas','bombones','barquillos','caramelos','sobao','kikos','cookies','pionono','gominolas','amarettis','toffee','ron','brandy','cerveza','coñac','cava','vodka','sidra','whisky','tequila','aguardiente','ginebra','vermut','mirin','sake','amaretto','baileys','kirsch','bíter','pisco','champagne','rompope','marsala','curaçao','limoncello','calvados','chicha','martini','mezcal','pulque','cachaça','mosto','ajenjo','txakoli','malibú','pacharán','armagnac','sambuca','chartreuse','drambuie','aperol','midori','sangría','gaseosa','limonada','tónica','refresco','horchata','sprite','clamato','infusión','capuchino','mate','kombucha','pepsi'
]

def create_recipes_and_save_csv(n_recipe, minimum_amount_of_ingredients, maximum_amount_of_ingredients, fname='crazy_recipes'):
    global ingredients
    
    recipes = dict([('recipe', []), ('ner', [])])
    
    for (n, i) in generate_recipes(n_recipe, ingredients, minimum_amount_of_ingredients, maximum_amount_of_ingredients).items():
        recipes['recipe'].append(n)
        recipes['ner'].append(i)
        
    df = pd.DataFrame.from_dict(recipes)
    df.to_csv('data/' + fname + '.csv', index=False, sep='|')
    
