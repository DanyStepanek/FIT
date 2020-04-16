Testovací scénáře
=================

### Autor

Daniel Štěpánek xstepa61@stud.fit.vutbr.cz

### Testovací cíl

Testovanou aplikací je instance eCommerce platforma OpenCart. Reference:
http://docs.opencart.com/en-gb/introduction/

### Testované funkce

**Vstupní podmínky platné pro všechny scénáře** - Přístup do
administrátorské sekce - Testovací prostředí: /home/users - Minimální
počet uživatelských skupin: 2

**Přidání uživatelů**  
Scénáře: add\_user.feature - Přidat uživatele: uživatel je přidán -
Přidat uživatele s již existující přezdívkou do jiné skupiny uživatelů:
uživatel je přidán - Přidat uživatele s již existující přezdívkou:
uživatel není přidán - Přidání uživatele s nevalidně vyplněnými údaji:
uživatel není přidán

**Odebrání uživatelů**  
Scénáře: delete\_user.feature - Odstranění uživatele: uživatel odstraněn
- Odstranění uživatele s prázdným výběrem: žádný uživatel není odstraněn

**Editace informací uživatele**  
Scénáře: edit\_user.feature - Změna informací (validní informace):
informace změněny - Změna skupiny uživatelů uživatele: skupina změněna -
Změna informací (nevalidní informace): informace nezměněny
