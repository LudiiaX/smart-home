# smart-home
# API de Gestion d'État de Prise / Ordinateur

Cette API permet de **consulter et piloter l’état d’une prise électrique et de l’ordinateur qui y est connecté**.  
Elle expose des endpoints simples pour **on**, **off** et **status** du système.

---

## 📌 Fonctionnement général

L’API repose sur un **état unique** représentant la situation actuelle de la prise et de l’ordinateur.

Chaque requête retourne un **code d’état numérique** accompagné d’une description lisible.

---

## 🔢 États possibles de l’API

| Code | Signification |
|----|--------------|
| **-1** | Inconnu (état non déterminé ou erreur) |
| **0** | Prise éteinte |
| **1** | Prise allumée |
| **2** | Ordinateur allumé |

---

## 🌐 Base URL

[text](http://localhost:8000)


