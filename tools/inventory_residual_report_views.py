# -*- coding: utf-8 -*-
# =============================================================================
# INVENTAIRE (LECTURE SEULE) DES VUES RAPPORTS RÉSIDUELLES POST-MIGRATION v15
# -----------------------------------------------------------------------------
# Contexte : la base staging Smarteo a été migrée depuis la v15. Les fichiers
# rapport de smt_sale / softeo_report / smt_report (report_invoice_inherit) ont
# été SUPPRIMÉS du code (commit [REM]), mais les enregistrements ir.ui.view
# correspondants restent probablement en base : la suppression des fichiers ne
# supprime PAS les vues déjà chargées. Ce script les recense pour décision
# manuelle (archivage ou suppression), vue par vue.
#
# À exécuter dans le shell Odoo.sh du staging. Voir tools/README.md.
# Ce script ne fait AUCUNE écriture (pas de create/write/unlink, pas de commit).
# Il se contente de lire ir.ui.view et d'imprimer un rapport texte.
# =============================================================================

# Templates de base dont on veut lister les héritières.
BASES = [
    "sale.report_saleorder_document",
    "account.report_invoice_document",
    "stock.report_delivery_document",
    "web.external_layout_boxed",
    "web.address_layout",
]

# Vue non filtrée par 'active' : les vues résiduelles peuvent être active=False.
View = env["ir.ui.view"].with_context(active_test=False)

out = []
def w(line=""):
    out.append(line)

def excerpt(view, n=200):
    """200 premiers caractères de l'arch (espaces normalisés)."""
    try:
        arch = view.arch or ""
    except Exception as exc:  # arch illisible (ex. xpath cassé)
        return "<arch illisible: %s>" % exc
    return " ".join(str(arch).split())[:n]

def xml_id_of(view):
    try:
        return view.get_external_id().get(view.id) or "(sans xml_id)"
    except Exception:
        return "(xml_id indéterminé)"

def dump(view):
    w("  " + "-" * 68)
    w("  id=%s  active=%s  write_date=%s" % (view.id, view.active, view.write_date))
    w("  name    : %s" % view.name)
    w("  xml_id  : %s" % xml_id_of(view))
    inh = view.inherit_id
    w("  inherit : %s" % (xml_id_of(inh) if inh else "-"))
    w("  arch200 : %s" % excerpt(view))

w("=" * 70)
w("INVENTAIRE VUES RAPPORTS RÉSIDUELLES (LECTURE SEULE)")
w("Base de données : %s" % env.cr.dbname)
w("=" * 70)

for base_xmlid in BASES:
    w("")
    w("#" * 70)
    w("# BASE : %s" % base_xmlid)
    base = env.ref(base_xmlid, raise_if_not_found=False)
    if not base:
        w("  (template de base introuvable dans cette base)")
        continue
    w("  base view : id=%s  name=%s" % (base.id, base.name))

    # Descendants récursifs (héritage direct ET indirect, actifs et inactifs).
    seen, children, frontier = set(), View.browse(), View.search([("inherit_id", "=", base.id)])
    while frontier:
        fresh = frontier.filtered(lambda v: v.id not in seen)
        for v in fresh:
            seen.add(v.id)
        children |= fresh
        frontier = View.search([("inherit_id", "in", fresh.ids)]) if fresh else View.browse()

    if not children:
        w("  (aucune vue héritière)")
        continue
    w("  %s vue(s) héritière(s) :" % len(children))
    for v in children.sorted(lambda r: r.id):
        dump(v)

# Recherche libre : toute vue contenant "Optional Products".
w("")
w("#" * 70)
w('# RECHERCHE : vues contenant "Optional Products"')
opt = View.search([("arch_db", "ilike", "Optional Products")])
if not opt:
    w('  (aucune vue ne contient "Optional Products")')
else:
    w("  %s vue(s) trouvée(s) :" % len(opt))
    for v in opt.sorted(lambda r: r.id):
        dump(v)

report = "\n".join(out)
print(report)

# Pour écrire aussi dans un fichier (décommenter) :
# with open("/tmp/inventaire_vues_rapports.txt", "w") as fh:
#     fh.write(report)
#     print("\n[écrit dans /tmp/inventaire_vues_rapports.txt]")
