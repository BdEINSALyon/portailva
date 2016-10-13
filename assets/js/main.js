/**
 * Created by leo on 13/10/2016.
 */
$(document).ready(function() {
  $('table[id^=prettyTable]').DataTable({
    "language": {
      "lengthMenu": "Afficher _MENU_ enregistrements par page",
      "zeroRecords": "Aucun enregistrement correspondant",
      "info": "Page _PAGE_ sur _PAGES_",
      "infoEmpty": "Aucun enregistrement",
      "infoFiltered": "(recherche effectuée sur _MAX_ enregistrements)",
      "paginate": {
        "first": "Début",
        "last": "Fin",
        "next": "Suivant",
        "previous": "Précédent"
      },
      "thousands": " ",
      "decimal": ",",
      "search": "Rechercher :",
      "aria": {
        "sortAscending": ": trier par ordre croissant",
        "sortDescending": ": trier par ordre décroissant"
      }
    },
    "order": [[0, "asc"]]
  });
});