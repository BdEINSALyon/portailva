/**
 * Created by leo on 13/10/2016.
 */
$(function () {
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

    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    $('.searchbox-input').change(function () {
        $('.card').show();
        var filter = $(this).val(); // get the value of the input, which we filter on
        $('.container').find(".card-title:not(:contains(" + filter + "))").parent().parent().css('display', 'none');
    });
});