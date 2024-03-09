
function updateFilteredRowCount(tbody_id) {
    const tableRows = document.getElementById(tbody_id).getElementsByTagName('tr');
    var filteredRowCount = 0;

    for (var i = 0; i < tableRows.length; i++) {
        if (tableRows[i].style.display !== 'none') {
            filteredRowCount++;
        }
    }
    // Update the HTML element with the filtered row count
    document.getElementById(`filteredRowCount_${tbody_id}`).textContent = filteredRowCount;

    ///// hide the header "0 MEP deselected if at 0"
    if (filteredRowCount == 0 && tbody_id == "sortedOut_tbody") {
        document.getElementById('x_mep_deselected_header').style.display = 'none';
    } else {
        document.getElementById('x_mep_deselected_header').style.display = 'table-header-group';
    }
}

function removeDiacritics(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}


function filterTwoTables() {
    filterTable('summary_tbody')
    filterTable('sortedOut_tbody')
}


function filterTable(tbody_id) {
    let displayOfSorted
    let defaultDisplay

    if (tbody_id == 'summary_tbody') {
        displayOfSorted = 'none';
        defaultDisplay = 'table-row';
    } else if (tbody_id == 'sortedOut_tbody') {
        // the opposite of above
        displayOfSorted = 'table-row'; 
        defaultDisplay = 'none'; 
    }

    const tbody = document.getElementById(tbody_id);
    const numRows = tbody.rows.length;
    const numCols = tbody.rows[0].cells.length - 2; //exclude the 2 first cols
    const rows = document.querySelectorAll(`#${tbody_id} .votes_rows`);

    const filterValue = removeDiacritics(document.getElementById('filterInput').value.toLowerCase());

    for (const row of rows) {
        row.style.display = defaultDisplay;
    }

    /// sort on thumbs
    for (let iCol = 1; iCol <= numCols; iCol++) {
        var imgChoice = document.querySelector(`.col_${iCol}_set`).classList;
        imgChoice = Array.from(imgChoice).find(item => item.startsWith('thumb_'));
        const votes = document.querySelectorAll(`.col_${iCol}`);
        const oppositeChoice = (imgChoice === 'thumb_for') ? 'thumb_ag' : 'thumb_for';

        if (imgChoice == 'thumb_for' || imgChoice == 'thumb_ag') {
        // then you have to sort each rows
            for (let iRow = 0; iRow < numRows; iRow++) {
                const vote = Array.from(votes[iRow].classList).find(item => item.startsWith('thumb_'));
                if (vote == oppositeChoice) {
                    rows[iRow].style.display = displayOfSorted;
                }
            }
        }
    }

    /// sort on text
    rows.forEach(function (row) {
        var name = row.querySelector('td:nth-child(2)');
        var group = row.querySelector('.eu_party');
        var party = row.querySelector('td:nth-child(3)'); // Assuming party is in the third cell

        if (name && group && party) {
            // console.log(filterValue)
            name = removeDiacritics(name.textContent.toLowerCase());
            group = removeDiacritics(group.textContent.toLowerCase());
            party = removeDiacritics(party.textContent.toLowerCase());

            if (!(name.includes(filterValue) || group.includes(filterValue) || party.includes(filterValue))) {
                row.style.display = displayOfSorted;
            }
        }
    });

    updateFilteredRowCount(tbody_id);
}


// write cookie for 1 column
function writeCookie(icon) {
    icon = Array.from(icon); 
    let col = icon.find(item => item.startsWith('col_')) || '';
    let thumb = icon.find(item => item.startsWith('thumb')) || '';
    document.cookie = `${col}=${thumb}`;
}

function readCookie() {
    const cookies = document.cookie.split(';').map(cookie => cookie.trim());
    const cookieValues = {};
    for (const cookie of cookies) {
        if (cookie.startsWith('col_')) {
            const [col, position] = cookie.split('=');
            cookieValues[col] = position;
        }
    }
    return cookieValues;
}

// allow the toggling of icons in the buttons
document.addEventListener('DOMContentLoaded', function() {
    var toggleButtons = document.querySelectorAll('.toggleButton');
    const cookieValues = readCookie();

    toggleButtons.forEach(function(button) {
        var icon = button.querySelector('.toggleImage').classList;
        var text = button.querySelector('.toggleText');

        // read cookie and sort table at loading
        if (cookieValues[icon[2]] === 'thumb_for') {
            icon.replace('thumb_none', 'thumb_for');
            text.textContent = '';
        } else if (cookieValues[icon[2]] === 'thumb_ag') {
            icon.replace('thumb_none', 'thumb_ag');
            text.textContent = '';
        }
        filterTwoTables()

        // behaviour at choiceBtn click
        button.addEventListener('click', function() {
            if (icon.contains('thumb_for')) {
                icon.replace('thumb_for', 'thumb_ag');
            } else if (icon.contains('thumb_ag')) {
                icon.replace('thumb_ag', 'thumb_none');
                text.textContent = '?';
            } else if (icon.contains('thumb_none')) {
                icon.replace('thumb_none', 'thumb_for');
                text.textContent = '';
            }
            filterTwoTables()
            writeCookie(icon)
        });
    });
});


function resetStanceChoices() {
    var toggleButtons = document.querySelectorAll('.toggleButton');
    toggleButtons.forEach(function(button) {
        var icon = button.querySelector('.toggleImage').classList;
        var text = button.querySelector('.toggleText');
        // loop on all class items to find thumb_
        icon.forEach(function(item) {
            if (item.startsWith('thumb_')) {
                icon.remove(item);
            }
        });
        // Add the new class
        icon.add('thumb_none');
        text.textContent = '?';
        writeCookie(icon)
    });
    filterTwoTables()
}


// // Filter table with text form
document.addEventListener('DOMContentLoaded', function() {
    var filterInput = document.getElementById('filterInput');
    filterInput.addEventListener('input', filterTwoTables );
});


// show and hide the columns with the left and right arrow buttons
let currentColumnIndex = 0;
const tbody = document.getElementById('summary_tbody');
const numCols = tbody.rows[0].cells.length - 2; // Exclude the 2 first columns

function showColumn(index) {
    for (let iCol = 0; iCol < numCols; iCol++) {
        const thiscol = document.querySelectorAll(`.coll_${iCol}`);
        for (let j = 0; j < thiscol.length; j++) {
            if (iCol == index) {
                thiscol[j].style.display = 'table-cell';
            } else {
                thiscol[j].style.display = 'none';
            }
        }
    }
}

function showNextColumn() {
    currentColumnIndex = (currentColumnIndex + 1) % numCols;
    showColumn(currentColumnIndex);
}

function showPrevColumn() {
    currentColumnIndex = (currentColumnIndex - 1 + numCols) % numCols;
    showColumn(currentColumnIndex);
}

document.getElementById('nextBtn').addEventListener('click', showNextColumn);
document.getElementById('prevBtn').addEventListener('click', showPrevColumn);

showColumn(currentColumnIndex);


// apply min-width to tooltip_comment only if greater than 20 char
var elements = document.querySelectorAll('.tooltip');
elements.forEach(function (element) {
    const txtlen = element.textContent.length
    if (txtlen < 40) {
        element.style.minWidth = txtlen/2 + 'rem';
    } else {
        element.style.minWidth = '200px';
    }
  });


function clearFilterByText() {
    document.getElementById('filterInput').value = '';
    filterTwoTables();
}
document.getElementById('clearFilterButton').addEventListener('click', clearFilterByText);



//// given by Bulma's documentation to handle the general_help modal (except the last paragraph)
document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    function openModal($el) {
      $el.classList.add('is-active');
    }
  
    function closeModal($el) {
      $el.classList.remove('is-active');
    }
  
    function closeAllModals() {
      (document.querySelectorAll('.modal') || []).forEach(($modal) => {
        closeModal($modal);
      });
    }
  
    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);
  
      $trigger.addEventListener('click', () => {
        openModal($target);
      });
    });
  
    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
      const $target = $close.closest('.modal');
  
      $close.addEventListener('click', () => {
        closeModal($target);
      });
    });
  
    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
      if(event.key === "Escape") {
        closeAllModals();
      }
    });

    // custom: open the modal at loading of the summary page
    // const helping_modal = document.getElementById('general_help');
    // openModal(helping_modal);

});



// alert for AI translated languages
var languageCode = document.getElementById('language-code').getAttribute('data-language-code');
if (languageCode === 'nl') {
    alert("De huidige vertaling van Frans/Engels naar Nederlands is gemaakt door kunstmatige intelligentie. Als je een fout ziet, of als je gemotiveerd bent om de volledige vertaling te valideren, neem dan contact met me op.");
}

