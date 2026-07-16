# tools/ — utilitaires hors modules

Scripts d'exploitation, **non installés** par Odoo (ce dossier n'est pas un module
addon). À exécuter manuellement.

## inventory_residual_report_views.py

Inventaire **en lecture seule** des vues `ir.ui.view` résiduelles laissées en base
par la migration v15 → v19 (les fichiers rapport supprimés du code par le commit
`[REM]` ne suppriment PAS les enregistrements de vues déjà chargés en base).

Le script liste, pour chaque template de base rapport
(`sale.report_saleorder_document`, `account.report_invoice_document`,
`stock.report_delivery_document`, `web.external_layout_boxed`,
`web.address_layout`), toutes les vues héritières (héritage direct **et**
indirect, actives **et** inactives) avec : `id`, `name`, `xml_id` (le préfixe du
xml_id = module d'origine, ex. `smt_sale.*`, `softeo_report.*`), `active`,
`write_date`, et un extrait des 200 premiers caractères de `arch_db`.
Il recherche aussi toute vue dont l'`arch_db` contient « Optional Products ».

**Le script n'écrit rien** : aucun `create` / `write` / `unlink`, aucun `commit`.
Il produit uniquement un rapport texte sur la sortie standard.

### Exécution sur le shell Odoo.sh (branche staging `release`)

Ouvrir un shell sur la branche staging, puis, depuis la racine du dépôt :

```bash
# En une commande (le rapport est redirigé dans un fichier) :
odoo shell -d "$ODOO_DATABASE" --no-http < tools/inventory_residual_report_views.py > inventaire_vues.txt

# ... ou en collant le contenu du script dans un shell Odoo interactif :
odoo shell -d "$ODOO_DATABASE" --no-http
>>> exec(open("tools/inventory_residual_report_views.py").read())
```

Sur Odoo.sh le binaire peut s'appeler `odoo-bin` au lieu de `odoo`, et le nom de
la base est celui de la branche staging (visible dans l'interface Odoo.sh).

### Suite

Transmettre `inventaire_vues.txt`. La décision (archiver `active=False` vs
supprimer) sera prise **vue par vue** ensuite — ce script ne fait que constater.
La désinstallation éventuelle de `softeo_report` est une action séparée à mener
depuis Odoo après l'inventaire (hors périmètre de ce script).
