-- Question 19 

-- 1 a 
SELECT d.pays, sum(d.dispo_prot) * p.population as ratio
FROM dispo_alim d, population p
WHERE d.code_pays == p.code_pays AND d.année == p.année
group by d.pays
ORDER by ratio desc
limit 10
;


-- 1 b
SELECT d.pays, sum(d.dispo_alim_kcal_p_j) * p.population as ratio
FROM dispo_alim d, population p
WHERE d.code_pays == p.code_pays AND d.année == p.année
group by d.pays
ORDER by ratio desc
limit 10
;

-- 2
SELECT d.pays, d.année, sum(d.dispo_prot) * p.population as ratio
FROM dispo_alim d, population p
WHERE d.code_pays == p.code_pays AND d.année == p.année
group by d.année, d.pays
ORDER by ratio asc
LIMIT 10
;


-- 3
SELECT E.pays,E.année, sum(E.pertes) as pertes_total
FROM  equilibre_prod E
GROUP BY E.pays,E.année
ORDER by pertes_total desc
;


-- 4
SELECT P.pays, ((S.nb_personnes * 100) / P.population) as proportion
FROM  population P, sous_nutrition S
WHERE P.code_pays == S.code_pays AND P.année == S.année
GROUP BY P.pays
ORDER by proportion desc
limit 10
;


-- 5
SELECT E.produit,sum(E.autres_utilisations) / sum(E.dispo_int) as ratio
FROM  equilibre_prod E
GROUP BY E.produit
ORDER by ratio desc
limit 10
;