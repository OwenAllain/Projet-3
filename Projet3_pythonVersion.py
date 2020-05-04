#!/usr/bin/env python
# coding: utf-8

# # Livrable projet 3 : realisez une etude de sante publique 

# In[1]:


# Import des librairies
import numpy as np
import pandas as pd
import seaborn as sns

# Import des données des bilans alimentaires
veg = pd.read_csv("data/Bilan_alim_vegetal.csv")
ani = pd.read_csv("data/Bilan_alim_animal.csv")

# Ajout de la variable origin
ani["origin"] = "animal"
veg["origin"] = "vegetal"

# On regroupe veg et ani en un unique dataframe, via une union
temp = ani.append(veg)

# Suppression de ani et veg
del ani, veg

# On renomme les colonnes de temp
temp.columns = ["xx","xx2","country_code","country",'xx3','element'
    ,'item_code','item','xx4',"year","unit","value",'xx5','xx6'
    ,'origin']

# # Transformation de temp en table pivot
data = temp.pivot_table(
    index=["country_code","country","item_code","item","year","origin"],
    columns = ["element"], values=["value"], aggfunc=sum)
data = data.reset_index()
data.head()


# **Question 1 :**
# Donnez le résultat de votre calcul pour l'année 2013, 
# ainsi que pour la dernière année  disponible au jour où vous effectuez ce projet.
# 
# Dernière années disponible a ce jour : **2013**
# 
# Créez un dataframe contenant les informations de population de chaque pays. 
# Calculez le nombre total d’humains sur la planète. 
# Critiquez votre résultat. En cas d’anomalie, analysez et effectuer les corrections nécessaires.

# In[2]:


#Importe nos données
population_par_pays = pd.read_csv("data/Bilan_alim_Population.csv")

#Nettoye nos données
population_par_pays = population_par_pays[['Pays','Valeur']]

#On s'assure qu'il n'y est pas 2 fois le même pays
population_par_pays = population_par_pays.drop_duplicates('Pays',keep = 'first')

#On retire les information non nommer (NaN) ( Ici on retire une ligne si au moins un parametre est NaN)
population_par_pays.dropna(axis='index')

#On renome les colones
population_par_pays.columns=['country','population(1000 personnes)']



#Regarde nos valuers
population_par_pays.head()

#calcule de la popultaiton total sur terre (*1000 car l'unité precise que ces pour 1000 personne par unité de valeur)
population_total_sur_terre = population_par_pays['population(1000 personnes)'].sum() * 1000

print('La popultation humaine en 2013 etait de {} personnes'.format(population_total_sur_terre))


# Soit il y aurait eu environs 8 milliards de personnes sur terre ne 2013
# 
# Ce chiffre est un peut élevé, même si les chiffres sont arrondit, ici au millier de personnes. 
# Pourtant quand on regarde au cas par cas,chaque pays semble respecter ses chiffres comme par exemple l'afghanistan,
# nous avons 30 552 000 personnes et la banque modiale donne 31 700 000 personnes pour les même dates
# Mais en continuant notre investigation nous remarqu'on un petit details ici :

# In[3]:


population_par_pays.sort_values(by='population(1000 personnes)').tail()


# Nous pouvons voire que la chine est "compter deux fois", ici la chine continantal et la chine sont compter
# La chine continental represente la chine sans l'île de Taïwan et les îles voisines.
# Il serait donc ici plus judicieux de faire : 

# In[4]:


population_par_pays.loc[174,'population(1000 personnes)'] = population_par_pays.loc[174,'population(1000 personnes)'] - population_par_pays.loc[35,'population(1000 personnes)']


# In[5]:


pop_terre = population_par_pays['population(1000 personnes)'].sum()*1000
pop_terre


# Le resultats parait déjâ un plus probable que le précédent

# In[6]:


#Ajoute de la population au dataframe principale
data = pd.merge(data,population_par_pays,left_on='country', right_on='country', left_index=True, right_index=False)

#Renome les colones pour plus de claireter
data.columns = ['country','country_code','i_country','item_code','item',
               'year','origin', 'Aliments pour animaux','Autres Utilisations',
               'Disponibilité alimentaire (Kcal/personne/jour)',
               'Disponibilité alimentaire en quantité (kg/personne/an)',
               'Disponibilité de matière grasse en quantité (g/personne/jour)',
               'Disponibilité de protéines en quantité (g/personne/jour)',
               'Disponibilité intérieure','Exportations - Quantité','Importations - Quantité',
               'Nourriture','Pertes','Production','Semences','Traitement','Variation de stock','population(1000 personnes)']

#Supprime les colones inutiles
data = data.drop(columns='i_country')
data = data.reset_index()
data = data.drop(columns='index')
#On jete un petit coup d'oeil
data.head()


# **Question 2 :** 
# 
# Identifiez ces redondances, en donnant votre réponse sous forme de formule mathématique (pas besoin de coder ici). C'est une équation à 3 termes de type a1+a2+[...]=b1+b2+[...]=c1+c2+[...] ) faisant intervenir chacune des 11 quantités données ci dessus. 
# Illustrez cette équation avec l'exemple du blé en France. Pour avoir un indice, cliquez sur "Définitions et Standards" sur la page de téléchargement des données.
# 
# 
# Disponibilité interieur = (production + importation - exportation) + evoltion des stocks
# 
# Disponibilité par habitant = nourriture/ nombre d'habitant
# 
# Taux de dependance a l'importation = (importation*100)/(production +importation-exportation)
# 
# Nourriture = production + importation - (aliment pour annimaux + autre usage + perte)
# 
# Disponibilité = Disponibilié interieur + semence - perte
# 
# Disponibilité alimentaire( Kcal/personne ) = Disponibilité alimentaire (Kcal/personne/jour) * 365
# 
# Disponibilité alimentaire( Kcal ) = Disponibilité alimentaire( Kcal/personne) * populaiton
# 
# Disponibilité de matière grasse en quantité (g/personne) = Disponibilité de matière grasse en quantité (g/personne/jour)*365
# 
# Disponibilité de matière grasse en quantité (g) = Disponibilité de matière grasse en quantité (g/personne) * population
# 
# Disponibilité de protéines en quantité (g/personne) = Disponibilité de protéines en quantité (g/personne/jour)*365
# 
# Disponibilité de protéines en quantité (g) = Disponibilité de protéines en quantité (g/personne)*population
# 
# 
# 

# **Question 3 :**
#     
# Calculez (pour chaque pays et chaque produit) la disponibilité alimentaire en kcal puis en kg de protéines.
# Vous ferez cela à partir de ces informations :
# 
#   -Population de chaque pays
# 
#   -Disponibilité alimentaire ("Food Supply" en anglais) donnée pour chaque produit et pour chaque pays en kcal/personne/jour.
# 
#   -Disponibilité alimentaire en protéines ("Protein supply quantity" en anglais) donnée pour chaque produit et pour chaque pays en g/personne/jour.
# 

# In[7]:


data['Disponibilité alimentaire (Kcal)'] = (data['Disponibilité alimentaire (Kcal/personne/jour)'] * 365) * (data['population(1000 personnes)'] * 1000)

data['Disponibilité de protéines en quantité (kg)'] = ((data['Disponibilité de protéines en quantité (g/personne/jour)'] * 365) *(data['population(1000 personnes)'] * 1000))/1000


# In[8]:


#On regarde les données
data.head()


# **Question 4 :**
# 
# A partir de ces dernières informations, et à partir du poids de la disponibilité alimentaire 
# (pour chaque pays et chaque produit), calculez pour chaque produit le _ratio "énergie/poids"_, que vous donnerez en kcal/kg.
# 
# Vous pouvez vérifier la cohérence de votre calcul en comparant ce ratio aux données disponibles sur internet 
# par exemple en cherchant la valeur calorique d'un oeuf.

# In[9]:


#calcule ratio kcal / kg

data['ratio "énergie/poids"(kcal/kg)'] = data['Disponibilité alimentaire (Kcal)'] / (data['Nourriture']*1000000)


# En suivant la même méthodologie, calculez également le pourcentage de protéines de chaque produit (pour chaque pays). 
# Ce pourcentage est obtenu en calculant le _ratio "poids de protéines/poids total"_ (attention aux unités utilisées). Vous pouvez vérifier la cohérence de votre calcul en comparant ce ratio aux données disponibles sur internet, par exemple en cherchant la teneur en protéines de l'avoine.

# In[10]:


#Calcule du ratio "poids de protéines/poids total"

data['ratio "poids de protéines/poids total"'] = data['Disponibilité de protéines en quantité (kg)'] / (data['Nourriture']*1000000)


# In[11]:


#On jete un coup d'oeil au données
data.head()


# **Question 5 :**
#  Citez 5 aliments parmi les 20 aliments les plus caloriques, en utilisant le ratio énergie/poids. 
#  
# Étonnamment, il arrive que ce ratio soit différent en fonction du pays. 
# Il faudra donc réaliser pour chaque aliment une moyenne sur les différents pays. 
# Vous créerez donc une nouvelle table grâce à une agrégation. 
# Attention à bien retirer les valeurs égales à 0 afin de ne pas fausser le calcul de la moyenne.
# 
# Citez 5 aliments parmi les 20 aliments les plus riches en protéines.

# In[12]:


#On enlevve les donner non entiere
df_normalise = pd.DataFrame(data.drop(['country_code','item_code','year','origin','Aliments pour animaux',
                                       'Autres Utilisations','Disponibilité alimentaire (Kcal/personne/jour)',
                                       'Disponibilité alimentaire en quantité (kg/personne/an)','Pertes',
                                       'Production','Semences','Traitement','Variation de stock',
                                       'population(1000 personnes)','Disponibilité alimentaire (Kcal)',
                                       'Disponibilité de protéines en quantité (kg)',
                                       'Disponibilité de matière grasse en quantité (g/personne/jour)',
                                       'Disponibilité de protéines en quantité (g/personne/jour)',
                                       'Disponibilité intérieure','Exportations - Quantité',
                                       'Importations - Quantité','Nourriture'],axis=1))

df_normalise.head()


# In[13]:


#On remarque les valeurs 'inf' nous les remplaçons par nan car elle ne sont pas utile
pd.set_option('use_inf_as_na', True)


# In[14]:


#On met en forme le dataframe en retirant les valeurs inutiles.
df_normalise = df_normalise.dropna()
df_normalise = df_normalise[df_normalise['ratio "énergie/poids"(kcal/kg)']!=0.0]

# On prepare nos donnée pour l'agregation
gb_df_normalise = df_normalise.groupby('item')

#On fait la moyenne des produits, et on renome la colone
m = gb_df_normalise.mean()
m.columns = ['ratio moyen "énergie/poids" (kcal/kg)','ratio moyen "poids de protéines/poids total"']

#On cree un dataframe avec nos donnée
moy_ratio_normalise = pd.DataFrame(m)


# In[15]:


moy_ratio_normalise.sort_values('ratio moyen "énergie/poids" (kcal/kg)',ascending=False).head(20)


# In[16]:


moy_ratio_normalise.sort_values('ratio moyen "poids de protéines/poids total"',ascending=False).head(20)


# On peut donc siter pour les proteines : 
#     - soja
#     - arachides
#     - pois
#     - viande,Autre
#     - Viande de Bovins
# 
# On peut donc siter pour les calories : 
#     - Huiles de Foie de Poisso
#     - Huiles de Poissons
#     - Huile de Tournesol
#     - Huile d'Olive
#     - Huile Graines de Coton
# 

# Donnez les résultats des questions 6 à 14 pour l'année 2013 ainsi que pour la dernière année disponible dans les données de la FAO.
# 
# Dernière année disponible = 2013

# **Question 6 :**
# 
# Calculez, pour les produits végétaux uniquement, la disponibilité intérieure mondiale exprimée en kcal.

# In[17]:


#Calcule de la disponibiliter interieur en kcal / produits
data['Disponibilité intérieure(Kcal)'] = (data['Disponibilité intérieure'] * 1000000 ) * data['ratio "énergie/poids"(kcal/kg)']


# In[18]:


dispo_kcal_veg_monde = data[data['origin']=='vegetal']['Disponibilité intérieure(Kcal)'].sum()

print("Il y a {} kcal d'origine vegetal disponible dans le monde en 2013".format(int(dispo_kcal_veg_monde)))


# **Question 7 :**
#  
# Combien d'humains pourraient être nourris si toute la disponibilité intérieure mondiale de produits végétaux était utilisée pour de la nourriture ? 
# Donnez les résultats en termes de calories, puis de protéines, et exprimez ensuite ces 2 résultats en pourcentage de la population mondiale.

# On calcule la disponibiliter interieur en proteine pour les besoins de la question

# In[19]:


data['Disponibilité intérieure proteine (kg)'] = data['Disponibilité intérieure'] * 1000000 * data['ratio "poids de protéines/poids total"']      


# In[20]:


#Disponibiliter interieur en kg de proteine
dispo_prot_veg_monde = data[data['origin']=='vegetal']['Disponibilité intérieure proteine (kg)'].sum()

print("Il y a {} kg de proteine d'origine vegetal disponible dans le monde en 2013".format(int(dispo_prot_veg_monde)))


# Calculons ensuite combien d'humain on peut nourrire avec tout ca
# Nous prendrons ces humain type: 
# sources : 
# http://www.fao.org/docrep/007/y5686e/y5686e08.htm
# 
# Femme de 20 a 30 ans avec un style de vie normal (activiter physique moderer) et d'un poid moyen de 55kg : 
# 2 450 kcal/jours soit **894 250 kcal** en 1 an
# 
# Homme de 20 a 30 ans avec un style de vie normal (activiter physique moderer) et d'un poid moyen de 75kg : 
# 3 450 kcal/jours soit **1 259 250 kcal** en 1 an
# 
# **Un humain lambda : 2 500 kcal/jours soit __912 500kcal__ en 1 an
# 
# 
# 
# 
# Pour les proteine nous garderons nos humains type si dessus:
# sources : 
# https://www.cerin.org/actualites/besoin-en-proteines-des-sportifs-aspects-quantitatif-et-qualitatif/
#         
# Femme style de vie normal (sedentaire) 55kg : 0,83g/kg/j soit 45.65 g/j ou **16662.25 g** de proteine en 1 an (16.66225Kg)
# 
# Homme style de vie normal (sedentaire) 75kg : 0,83g/kg/j soit 62.25 g/j ou **22721.25 g** de proteine en 1 an (22.72125Kg)
# 
# Soit notre humain lambda a **19691.75 g** en 1 an (19.69175 kg)
# 
# 
# 

# In[21]:


#On arroundi un peut nos chiffres
humain_kcal = 912500
humain_prot = 20


nb_perosnne_kcal = int(dispo_kcal_veg_monde/humain_kcal)
nb_perosnne_prot = int(dispo_prot_veg_monde/humain_prot)


# In[22]:


print("On pourrait donc nourrire {} personnes avec les kcal et {} avec les proteine".format(nb_perosnne_kcal,nb_perosnne_prot))


# On passe le tout en pourcentage

# In[23]:


porcent_pop_kcal = int(nb_perosnne_kcal * 100 / pop_terre)
pourcent_pop_prot = int(nb_perosnne_prot * 100 / pop_terre)


# In[24]:


print('{} % de la population de kcal et {} % de pop en prot'.format(porcent_pop_kcal,pourcent_pop_prot))


# **Question 8 :** 
#     
# Combien d'humains pourraient être nourris si toute la disponibilité alimentaire en produits végétaux (Food) la nourriture végétale destinée aux animaux (Feed) et les pertes de produits végétaux (Waste) étaient utilisés pour de la nourriture ? 
# 
# Donnez les résultats en termes de calories, puis de protéines, et exprimez ensuite ces 2 résultats en pourcentage de la population mondiale.

# Disponibiliter mondiale en kcal vegetal en prennant les pertes et les aliments pour animaux

# In[25]:


dispo_kcal_veg_monde_total = (data[data['origin']=='vegetal']['Nourriture']+data[data['origin']=='vegetal']['Pertes']+data[data['origin']=='vegetal']['Aliments pour animaux']) * 1000000 * data[data['origin']=='vegetal']['ratio "énergie/poids"(kcal/kg)']


# In[26]:


dispo_kcal_veg_monde_total_sum = dispo_kcal_veg_monde_total.sum()
print('Il y a {} kcal vegetal'.format(dispo_kcal_veg_monde_total_sum))


# On fait de même pour les proteines

# In[27]:


dispo_prot_veg_monde_total = (data[data['origin']=='vegetal']['Nourriture'] + data[data['origin']=='vegetal']['Pertes'] + data[data['origin']=='vegetal']['Aliments pour animaux']) * 1000000 * data[data['origin']=='vegetal']['ratio "poids de protéines/poids total"']


# In[28]:


dispo_prot_veg_monde_total_sum = dispo_prot_veg_monde_total.sum()
print('Il y a {} prot vegetal'.format(dispo_prot_veg_monde_total_sum))


# On calcule le nombres d'humains nourrisable avec 
# en gardant le même _humain type_

# In[29]:


nb_perosnne_kcal_tt = int(dispo_kcal_veg_monde_total_sum/humain_kcal)
nb_perosnne_prot_tt = int(dispo_prot_veg_monde_total_sum/humain_prot)

#En pourcentage
pourcent_pop_kcal_tt = int(nb_perosnne_kcal_tt * 100 / pop_terre)
pourcent_pop_prot_tt = int(nb_perosnne_prot_tt * 100 / pop_terre)


# In[30]:


print('{} % de la population de kcal et {} % de pop en prot'.format(pourcent_pop_kcal_tt,pourcent_pop_prot_tt))


# **Voire les resulat pour les prots**

# **Question 9 :** 
# 
# Combien d'humains pourraient être nourris avec la disponibilité alimentaire mondiale ? Donnez les résultats en termes de calories, puis de protéines, et exprimez ensuite ces 2 résultats en pourcentage de la population mondiale.

# On reprendre les meme calcule que la question précédente sans filter uniquement les vegetaux .

# In[68]:


dispo_kcal_monde_total = data['Nourriture'] * data['ratio "énergie/poids"(kcal/kg)']
dispo_kcal_monde_total_sum = dispo_kcal_monde_total.sum()

dispo_prot_monde_total = data['Nourriture'] * 1000000 * data['ratio "poids de protéines/poids total"']
dispo_prot_monde_total_sum = dispo_prot_monde_total.sum()


# In[69]:


nb_perosnne_kcal_monde = int(dispo_kcal_monde_total_sum/humain_kcal)
nb_perosnne_prot_monde = int(dispo_prot_monde_total_sum/humain_prot)

#En pourcentage
pourcent_pop_kcal_monde = int(dispo_kcal_monde_total_sum * 100 / pop_terre)
pourcent_pop_prot_monde = int(dispo_prot_monde_total_sum * 100 / pop_terre)


# In[70]:


print('{} % de la population de kcal et {} % de pop en prot'.format(pourcent_pop_kcal_monde,pourcent_pop_prot_monde))


#  **Question 10 :**
#         
# A partir des données téléchargées qui concernent la sous-nutrition, répondez à cette question : Quelle proportion de la population mondiale est considérée comme étant en sous-nutrition ?

# Preparont un dataframe des données de sous nutrission.
# 

# In[34]:


#importation
data_secu = pd.read_csv('data/DonneeSec_Personne_sousAlimenter.csv')

#On modifie la chine comme fait pour la question 1
data_secu.loc[data_secu['Zone'] == 'Chine','Valeur'] = data_secu[data_secu['Zone'] == 'Chine']['Valeur'] - data_secu[data_secu['Zone'] == 'Chine, continentale']['Valeur']

#Regarde la forme des données
data_secu.head()


# Les colones sont assez explixite donc il n'y a pas besoin de les renommées

# La question est la suivante : Quelle proportion de la population mondiale est considérée comme étant en sous-nutrition ?
#     Pour ce faire nous allons simplement additionner toute les personnes sous alimenter presente dans ce tableau : "Nombre de personnes sous-alimentées (millions)"
#      et en faire un pourcentage de la population mondiale total que nous avons trouver dans les questions precedentes

# In[35]:


nb_personne_sous_alim = data_secu[data_secu["Produit"]=="Nombre de personnes sous-alimentées (millions) (moyenne sur 3 ans)"]['Valeur'].sum()

print("soit il y aurait {} millions de personnes soufrant de sous alimentation dans le monde".format(nb_personne_sous_alim))


# In[36]:


#On ramene notre population en uniter et on la passe en % de la population du monde.
nb_personne_sous_alim_pourcent  = nb_personne_sous_alim * 1000000 * 100 / pop_terre

print('Ce qui represente donc {} % de la population'.format(int(nb_personne_sous_alim_pourcent)))


# Établissez la liste des produits (ainsi que leur code) considéré comme des céréales selon la FAO.
# 
# Repérez dans vos données les informations concernant les céréales (par exemple en créant une colonne de type booléen nommée "is_cereal").
# 
# Nous allons donc ajouter une colone a notre dataframe _data_ nommer "is_cereal" qui sera un booléen, il sera _True_ si le produit est un céréale.

# In[37]:


# Import des données des céréales seulement
temp_data_cereal = pd.read_csv('data/Bilan_alim_cerealBiere.csv')

#Petite table pivot rapide pour recupere la meme mise en forme que le dataframe principale
temp_data_cereal = temp_data_cereal.pivot_table(
    index=["Code Pays","Pays","Code Produit","Produit","Année"],
    columns = ['Élément'], values=["Valeur"], aggfunc=sum)

temp_data_cereal = temp_data_cereal.reset_index()

#Isole les colones qu'on veut
a = pd.unique(temp_data_cereal['Code Produit'])
b = pd.unique(temp_data_cereal['Produit'])

#Crée un dataframe avec les codes et les produit
df_liste_cereal = pd.DataFrame({'item_code':a,'item':b})


# Nous avons donc la liste des produits considere comme céréale par le fao 

# In[38]:


df_liste_cereal


# Il nous faut mainteant crée notre colone sur le dataframe principale et la remplire correctement

# In[39]:


#On separe pour plus de claireter
f = data['item_code'].isin(df_liste_cereal['item_code'])

#On remplis la colones avec les valeur qui sont connu
data.loc[f,'is_cereal']=True

#Et on mes les false a la place des nan qui arrive par defaut
data['is_cereal'] = data['is_cereal'].fillna(False)


# In[40]:


#On jete un coup d'oeil
data[['country','item','is_cereal']].head(10)


# **Question 11 :**
# 
# En ne prenant en compte que les céréales destinées à l'alimentation (humaine et animale), quelle proportion (en termes de poids) est destinée à l'alimentation animale ?

# In[41]:


#Calcule le nb de kg de céréale pour animaux
cereal_animau_total_pds = data[data['is_cereal']]['Aliments pour animaux'].sum() * 1000000

#Calcule le nb de kg de céréale pour alimentation ( animaux et humains)
cereal_alimentation = data[data['is_cereal']]['Aliments pour animaux'] + data[data['is_cereal']]['Nourriture']
cereal_alimentation_total_pds = cereal_alimentation.sum() *1000000

#On fait un pourcentage du poids des cereale pour animaux en fonction du poids total
taux_cereal_animal = cereal_animau_total_pds * 100 / cereal_alimentation_total_pds
print("Ainsi les animaux on {} % de la totaliter des céréales a destination de l'alimentation".format(int(taux_cereal_animal)))


# **Preparation suite**
# 
# Sélectionnez parmi les données des bilans alimentaires les informations relatives aux pays dans lesquels la FAO recense des personnes en sous-nutrition, pour une année choisie.(pourcentage par pays)
# 
# Repérez les 15 produits les plus exportés par ce groupe de pays sur l'année choisie.
# 
# Parmi les données des bilans alimentaires au niveau mondial, sélectionnez les 200 plus grandes importations de ces produits (1 importation = une quantité d'un produit donné importée par un pays donné sur l'année choisie)
# 
# Groupez ces importations par produit, afin d'avoir une table contenant 1 ligne pour chacun des 15 produits. Ensuite, calculez pour chaque produit les 2 quantités suivantes :
# 
# le ratio entre la quantité destinés aux "Autres utilisations" (Other uses) et la disponibilité intérieure.
# 
# le ratio entre la quantité destinée à la nourriture animale et la quantité destinée à la nourriture (animale + humaine)

# In[42]:


data = pd.merge(data,data_secu,left_on='country',right_on='Zone',how='left')
data = data.drop(['Code Domaine','Domaine', 'Code zone', 'Zone', 
                          'Code Élément', 'Élément','Code Produit', 'Produit', 
                          'Code année', 'Année', 'Unité','Symbole', 'Description du Symbole'],axis=1)


# In[43]:


data = data.rename(index=str,columns={'Valeur':'Nombre de personnes sous-alimentées (millions)'})
data['Pourcent population sous-alimnetées'] =( data['Nombre de personnes sous-alimentées (millions)'] * 1000000) * 100 / (data['population(1000 personnes)']*1000)
data.head()


# On a maintenant le pourcentage de personne sous alimenter par pays.

# In[44]:


#On selectionne tout les pays qui sont present dans la liste des pays avec de la sous alimentation
data_secu_sousalim = data[data['Pourcent population sous-alimnetées']>1]


# In[45]:


#On trie les valeurs par ordre decroissant de quantiter d'exportation
produit_plus_export = data_secu_sousalim.sort_values(['Exportations - Quantité'],ascending=False)

#On affiche les 15 premier produits
produit_plus_export[['country','item','Exportations - Quantité']].head(15)


# Parmi les données des bilans alimentaires au niveau mondial, sélectionnez les 200 plus grandes importations de ces produits (1 importation = une quantité d'un produit donné importée par un pays donné sur l'année choisie)
# 
#  Ici on doit trouver les 200 plus grande importation des produit que l'ont a trouver juste au dessus

# In[46]:


#On isole les produits les plus exporter
liste_produit_plus_export = produit_plus_export['item'].head(15).unique()


# In[47]:


#On prend les donner de data seulement pour les produits les plus exporter
produit_les_plus_import = data[data['item'].isin(liste_produit_plus_export)]

#On trie ces produits par quantiter d'import
produit_les_plus_import = produit_les_plus_import.sort_values(['Importations - Quantité'],ascending=False)

#On crée une variable pour les 200 plus gros import 
deux_cent_plus_gros_import = produit_les_plus_import[['country','item','Importations - Quantité']].head(200)
deux_cent_plus_gros_import.head(15)


# In[48]:


#On a tout nos produit trier par groupe de produit
produit_les_plus_import.sort_values(['item'],ascending=False).groupby('item').head()


# Calcule des ratio suivant:
# 
# le ratio entre la quantité destinés aux "Autres utilisations" (Other uses) et la disponibilité intérieure.
# 
# le ratio entre la quantité destinée à la nourriture animale et la quantité destinée à la nourriture (animale + humaine)

# In[49]:


df_export = pd.DataFrame(produit_les_plus_import.sort_values(['item'],ascending=False))
d = pd.pivot_table(produit_les_plus_import,index='item')
d = d.drop(['Disponibilité alimentaire (Kcal)',
       'Disponibilité alimentaire (Kcal/personne/jour)',
       'Disponibilité alimentaire en quantité (kg/personne/an)',
       'Disponibilité de matière grasse en quantité (g/personne/jour)',
       'Disponibilité de protéines en quantité (g/personne/jour)',
       'Disponibilité de protéines en quantité (kg)',
        'Disponibilité intérieure proteine (kg)',
       'Disponibilité intérieure(Kcal)', 'Exportations - Quantité',
       'Importations - Quantité', 'Pertes', 'Production',
       'Semences', 'Traitement', 'Variation de stock', 'country_code',
       'is_cereal', 'item_code', 'population(1000 personnes)',
       'ratio "poids de protéines/poids total"',
       'ratio "énergie/poids"(kcal/kg)', 'year'],axis=1)


# In[50]:


d['ratio"Autres utilisations" (Other uses)/disponibilité intérieure'] = d['Autres Utilisations']/d['Disponibilité intérieure']
d['ratio  nourriture animale/quantité nourriture(animale + humaine)'] = d['Aliments pour animaux']/d['Nourriture']


# In[51]:


d.head()


# **Question 12 :**
#     
# Donnez les 3 produits qui ont la plus grande valeur pour chacun des 2 ratios (vous aurez donc 6 produits à citer)

# In[52]:


d.sort_values('ratio"Autres utilisations" (Other uses)/disponibilité intérieure',ascending=False).head(3)


# In[53]:


d.sort_values('ratio  nourriture animale/quantité nourriture(animale + humaine)',ascending=False).head(3)


# **Question 13 :**
# 
# Combien de tonnes de céréales pourraient être libérées si les USA diminuaient leur production de produits animaux de 10% ?

# In[54]:


test1 = data[data['country']=="États-Unis d'Amérique"]

test1 = test1[test1['is_cereal']]

k = test1['Aliments pour animaux'].sum()


# In[55]:


j = k * 10 / 100
print("On pourrait libéré {} tonnes de cereals".format(j))


# **Question 14 :**
#     
# En Thaïlande, quel proportion de manioc est exportée ? Quelle est la proportion de personnes en sous-nutrition?

# In[56]:


manioc_thai = data[(data['country']=='Thaïlande') & (data['item']=='Manioc')]
manioc_thai_export = manioc_thai['Exportations - Quantité']
manioc_thai_total = manioc_thai['Production']


# In[57]:


proportion_export = manioc_thai_export * 100 / manioc_thai_total


# In[58]:


print("La Thaïlande exporte {} % de ca production de manioc".format(int(proportion_export.values)))


# In[59]:


p = data[data['country']=='Thaïlande']['Pourcent population sous-alimnetées'].unique()
print("La Thaïlande a {} % de personne en sous nutrission".format(int(p)))


# La partie calculatoire etant fini, nous allons exporter nos données.Mais il nous faut deja les preparer a l'export. Nous allons donc crée 4 fichier d'export.

# In[60]:


#Table population
df_pop = pd.DataFrame(data[['country', 'country_code','year','population(1000 personnes)']])
df_pop = df_pop.drop_duplicates()

#Table disponibiliter alimentaire
df_dispo = pd.DataFrame(data[['country', 'country_code','year', 'item', 'item_code', 'origin','Disponibilité intérieure','Disponibilité alimentaire (Kcal/personne/jour)','Disponibilité de matière grasse en quantité (g/personne/jour)','Disponibilité de matière grasse en quantité (g/personne/jour)']])

#Table equilibre de production
df_prod = pd.DataFrame(data[['country', 'country_code','year', 'item', 'item_code','Disponibilité intérieure','Aliments pour animaux','Semences','Pertes','Traitement','Nourriture','Autres Utilisations']])

#Table personnes sous alimenter
df_sousali = pd.DataFrame(data[['country', 'country_code','year','Nombre de personnes sous-alimentées (millions)']])
df_sousali = df_sousali.drop_duplicates()


# In[61]:


df_pop.to_csv("pop.csv", index = False)
df_dispo.to_csv("dispo.csv", index = False)
df_prod.to_csv("prod.csv", index = False)
df_sousali.to_csv("sousalim.csv", index = False)


# In[ ]:




