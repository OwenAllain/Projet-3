-- Question 15 à 18

CREATE TABLE dispo_alim (
    pays                STRING NOT NULL,
    code_pays           INTEGER NOT NULL,
    année               INTEGER NOT NULL,
    produit             STRING NOT NULL,
    code_produit        INTEGER NOT NULL,
    origin              STRING NOT NULL, 
    dispo_alim_tonnes   DOUBLE,
    dispo_alim_kcal_p_j DOUBLE,
    dispo_prot          DOUBLE,
    dispo_mat_gr        DOUBLE,
    CONSTRAINT PK_dispo_alim PRIMARY KEY (code_pays,année,code_produit),
    CONSTRAINT UC_dispo_alim UNIQUE (code_pays,année,code_produit)

 
);

CREATE TABLE equilibre_prod (
    pays                STRING NOT NULL,
    code_pays           INTEGER NOT NULL,
    année               INTEGER NOT NULL,
    produit             STRING NOT NULL,
    code_produit        INTEGER NOT NULL,
    dispo_int           DOUBLE,
    alim_ani            DOUBLE,
    semences            DOUBLE,
    pertes              DOUBLE,
    transfo             DOUBLE,
    nourriture          DOUBLE,
    autres_utilisations DOUBLE,
    CONSTRAINT PK_equilibre_prod PRIMARY KEY (code_pays,année,code_produit),
    CONSTRAINT UC_equilibre_prod UNIQUE (code_pays,année,code_produit)
);

CREATE TABLE population (
    pays       STRING NOT NULL,
    code_pays  INTEGER NOT NULL,
    année      INTEGER NOT NULL,
    population INTEGER,
    CONSTRAINT PK_population PRIMARY KEY (code_pays,année),
    CONSTRAINT UC_population UNIQUE (code_pays,année)
);

CREATE TABLE sous_nutrition (
    pays         STRING NOT NULL,
    code_pays    INTEGER NOT NULL,
    année        INTEGER NOT NULL,
    nb_personnes DOUBLE,
    CONSTRAINT PK_sous_nutrition PRIMARY KEY (code_pays,année),
    CONSTRAINT UC_sous_nutrition UNIQUE (code_pays,année)
);