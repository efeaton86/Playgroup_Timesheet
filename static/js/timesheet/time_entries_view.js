monthFilterButtons = document.querySelectorAll('.month_filter')

const filterCSSHighlight = " border border-2 border-bottom-0 rounded-top"
var filteredMonth = null
var filteredYear = null

monthFilterButtons.forEach(button => button.addEventListener(
    'click',
    function (e) {
        e.preventDefault()
        if (filteredMonth === null) {
            button.className += filterCSSHighlight
            button.setAttribute("id", "filtered_month")
            filteredMonth = button.dataset.month
            console.log('filteredMonth', filteredMonth)
        }
        else {
            // assign id to filtered month
            document.getElementById('filtered_month').className = "nav-link month_filter"
            document.getElementById('filtered_month').setAttribute("id", "")
            button.setAttribute("id", "filtered_month")
            button.className += filterCSSHighlight
            filteredMonth = button.dataset.month
            console.log('filteredMonth', filteredMonth)
        }



        // button.className = "nav-link month_filter"

        // button.className += filterCSSHighlight
        // filteredMonth = button.dataset.month
        // console.log('filteredMonth', filteredMonth)
    }
))
