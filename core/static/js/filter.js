$(document).ready(function(){
"use strict"


const updateFilterElement = (elemType, objElem) => {
    switch (elemType) {
        case 'toggleActive':
            let newTargetElem = document.querySelector(`option[value=${objElem.target.value}]`)
            newTargetElem.setAttribute('selected', 'selected')
    };
}

const getElem = (selector) => {
    let e = document.querySelector(`${selector}`);

    return e != null ? e : '' };

const getFilterState = (status) => {
        let result;
        
        if (status === 'default') {
            let sortBtn = document.getElementById('filter-submit-btn');
            let resetBtn = document.getElementById('filter-reset-btn');
            let genreElement = document.querySelector('#genre')
            let sortElement = document.querySelector('#sort')

            result = {
                "sortBtn": sortBtn,
                "resetBtn": resetBtn,
                "genreElement": genreElement,
                "sortElement": sortElement
            }

        } else {
            let genreElement = getElem('#genre option[selected="selected"]')
            let sortElement = getElem('#sort option[selected="selected"]')
            
            result = {
                "genreElement": {"title": genreElement.text, "slug": genreElement.value},
                "sortElement": {"title": sortElement.text, "slug": sortElement.value},
            }
        }

        return result
};

const updateCollection = (init) => {
    let state = getFilterState();

    let request = {
        "genre": state.genreElement,
        "sort": state.sortElement,
    };

    if (init) {
        $.ajax({
            type: 'GET',
            url: "/filter",
            data: JSON.stringify({}),
            dataType: 'html',
            success: (response) => {
            $("#media-collections").html(response)               
            },
            error: () => {
                alert("ERROR")
            }
        });
    } else {

        $.ajax({
            type: 'GET',
            url: "/filter",
            data: JSON.stringify({request}),
            dataType: 'html',
            success: (response) => {
                $("#media-collections").html(response)
            },
            error: () => {
                alert("ERROR")
            }
        });
    }

        
}

const initDefaultState = () => {

        let state = getFilterState('default');
        updateCollection('init');
        
        state.genreElement.addEventListener('change', (event) => {

            let node = document.querySelectorAll(`#${event.target.name} > option`)
            
            node.forEach(element => {
                if (element.hasAttribute('selected')) {
                    element.removeAttribute('selected')
                }
            });

            updateFilterElement('toggleActive', event);
            updateCollection();
            
        });

        state.sortElement.addEventListener('change', (event) => {
            let node = document.querySelectorAll(`#${event.target.name} > option`);
            
            node.forEach(el => {
                if (el.hasAttribute('selected')) {
                    el.removeAttribute('selected')
                }
            });

            updateFilterElement('toggleActive', event);
            updateCollection();
            
        });

        state.sortBtn.addEventListener('click', function(){
            updateCollection();
        });
}

initDefaultState()
});
