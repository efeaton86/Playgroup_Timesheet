

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////DOM SELECTORS/////////////////////////////////////////
var timeEntryForm = document.getElementById('timeEntryForm')
var addEntryFormRow = document.getElementById('timeEntry_addRow')
var removeEntryFormRow = document.getElementById('timeEntry_removeRow')
var svg = document.getElementById('svg_up')
var calendarDays = [...document.getElementsByTagName('td')]



const formRowCount = {
    count: 0,
    addOne: function () {
        return this.count += 1
    },
    subtractOne: function () {
        return this.count -= 1
    }
}

var counter = 0

////////////////////////////////////////////////////////////////////////////////////
////////////////////////////VARIABLES//////////////////////////////////////////////
const timeEntryFormRow = `
<div class="row">
    <input type="hidden" id="formIDX" name="formIDX" value="${counter}"/>
    <div class="col-3">
        <label for="date">Date</label>
        <input name="date" id="date" type="date" class="form-control" placeholder="Date">
    </div>
    <div class="col-2">
        <label for="hours">Hours</label>
        <input name="hours" id="hours" type="number" class="form-control" min="0">
    </div>
    <div class="col-2">
        <label for="minutes">Minutes</label>
        <input name="minutes" id="minutes" type="number" class="form-control" min="0">
    </div>
    <div class="col-3">
        <label for="comments">Comments</label>
        <textarea name="comments" id="comments" rows="1" class="form-control"></textarea>
    </div>
    <div class="col-2 justify-content-center me-0">
        <label for="overtime"></label>
        <select name="overtime" class="form-select" aria-label="Default select example" required>
          <option value="0">Base</option>
          <option value="1">Overtime</option>
        </select>
    </div>
</div>
`
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////EVENT LISTENERS/////////////////////////////////////////


addEntryFormRow.addEventListener('click', function () {
    counter += 1
    timeEntryForm.insertAdjacentHTML('afterbegin', timeEntryFormRow)
    timeEntryForm.getElementsByTagName('input')[0].setAttribute('value', counter)
})

removeEntryFormRow.addEventListener('click', function () {
    console.log('remove row')
    counter -= 1
    timeEntryForm.removeChild(timeEntryForm.getElementsByTagName('div')[0])
})

//select all of the days (td elements) of the calendar

const selectedDays = {
    daysSelectedArray: [],
    addDays: function(day) {
        if (this.daysSelectedArray.includes(day.id)) {
            return
        } else {
            this.daysSelectedArray.push(day.id)
            console.log(this.daysSelectedArray)
        }

    },
//     removeDays: function(day) {
//         dayIDX = this.daysSelectedArray.indexOf(day)
//         this.daysSelectedArray.splice(dayIDX, 1)
//         console.log(this.daysSelectedArray)
//     }
}


calendarDays.forEach(
    function (day) {
        // add event listener to each one, passing in the day that was clicked
        day.addEventListener(
            'click',
            function() {
            //  get the id of the days that were clicked
                selectedDays.addDays(day)
            }
        )
    }
)








