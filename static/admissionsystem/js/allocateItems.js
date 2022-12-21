function getCookie(name) //Cookie's value get from this function will use in ajax call
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//This function is use to display "Available Items" according to users' selected type.
//For example if user select "Computer" in Item Type then "Available Items" will show all items which
//is of type "Computer"
function getTypeRelatedItem() {
    var typeSelected = document.getElementById('itemTypeID').value //get Item Type that user choosed
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        // initialize an AJAX request
        url: '/getTypeRelatedItem',
        // set the url of the request
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            'typeSelected': typeSelected,
            'csrftoken': csrftoken,
        },

        success: function(data) {
            data = JSON.parse(data)
            console.log(data)
            var availItems = ""

            //below I am making an dyanamic option's string for all such items that user want to
            //see by choosing Item Type   
            for (name in data) {
                console.log(data[name])
                availItems += "<option>" + data[name] + "</option>";
            }
            //Here add that string to HTML datalist whose ID is availableitems
            ($("#availableitems")).html(availItems)
        }
    });

}


//This function get data(such items that user want to allocate to someone) from table and send it to
//views through views through AJAX call and there all data will be store in database
function getDataFromAllocateItemTable() {
    var table = document.getElementById('myTable')
    var assignTo = document.getElementById('assignToEmpName').value;
    if (assignTo == '') //If persons' name is missing to whom we are assigning
    {
        //document.getElementById('assignToEmpName').style.border = "1px solid red"
        alert('Select person to which you want to assign')
    } else if (table.rows.length - 2 == 0) //If table is empty
    {
        alert('Please add data to table')
    } else {
        empDataList = []
        tableDataList = []
        var todayDate = new Date();
        dic = { 'assignTo': assignTo, 'currentDate': todayDate } //make an dictonary object to send via AJAX
        empDataList.push(dic) //Dictonary object is store in list
        i = 1
        var totalPrice = 0

        /*
            In this loop, getting row wise data and make a dictonary object of one row and then store that
            dictonary object to list name "tableDataList". In list no of dictonary objects represent the 
            no of rows in table. Through AJAX, sending jsonify list. means sending a list in form of JSON
        */
        for (i; i < table.rows.length - 1; i = i + 1) {
            var itemName = table.rows[i].children[0].innerText;
            var itemType = table.rows[i].children[1].innerText;
            var dueDate = table.rows[i].children[2].innerText;
            var condition = table.rows[i].children[3].innerText;

            dic = {
                'itemName': itemName,
                'itemType': itemType,
                'dueDate': dueDate,
                'condition': condition
            }
            tableDataList.push(dic)

        }
        var empList = JSON.stringify(empDataList);
        var tableList = JSON.stringify(tableDataList);
        const csrftoken = getCookie('csrftoken');

        $.ajax({
            type: "POST",
            // initialize an AJAX request
            url: '/getDataFromAllocateItems',
            // set the url of the request
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                'empDataList': empList,
                'tableDataList': tableList,
                'csrftoken': csrftoken,
            },

            success: function(data) //this part is response of AJAX call from backend
                {

                    alert(data)
                    document.getElementById('assignToEmpName').value = ''

                    setTimeout(function() {
                        location.reload()
                    }, 80);
                }
        });
    }
}


// Logic for remove rows from table. Here oButton represent that row's button which wants to delete
function removeRow(oButton) {
    var empTab = document.getElementById('myTable');
    empTab.deleteRow(oButton.parentNode.parentNode.rowIndex);
    //here I getting row from button by accessing its parent
}


/*
    this function will check that which item user wants to allocate has not allocated yet. This function
    will iterate all table and match the name of current item with existing items that already
    in row to allocate to overcome the duplicate
*/
function isItemAlreadyAssigned(itemName) {
    var table = document.getElementById('myTable')

    i = 1
    for (i; i < table.rows.length - 1; i = i + 1) {
        if (table.rows[i].children[0].innerText == itemName) {
            alert('Item Already Assigned')
            return true
        }
    }
    return false

}

/* 
    This function will set the type of item as user choose the item from "Available Items". 
*/
function setItemType(curInput) {
    var itemCode = curInput.value;
    if (isItemAlreadyAssigned(itemCode)) //check for duplicate
    {
        alert("This item has already assigned")
        clearAllFields();
    } else {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            // initialize an AJAX request
            url: '/getItemType',
            // set the url of the request
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                'itemCode': itemCode,
                'csrftoken': csrftoken,
            },

            success: function(data) {
                //here data is the dictonary object which has two keys, itemType and itemCondition
                var select = curInput.parentNode.parentNode.children[1].children[0];
                //select represent the select HTML tag for dropdown list for Item Type
                if (data == '--') //if user write unavailable item
                {
                    select.selectedIndex = 0;
                } else {
                    data = JSON.parse(data) //parse the string into dictionary

                    //this loop will execute according to the no of types of items we have
                    for (let i = 0; i < select.options.length; i++) {

                        //IF CONDITION is checking if ith index of array of itemType is our required
                        //itemType which we want to select then it will assign that index to selectedIndex
                        if (select.options[i].value == data['itemType']) {
                            select.selectedIndex = i;
                        }
                    }

                    //below statement is for setting conditon of selected item
                    curInput.parentNode.parentNode.children[3].innerText = data['itemCondition']
                }


            }
        });
    }
}


document.getElementById('btnAddToTable').addEventListener('click', function(event) {
    event.preventDefault();
    addToTable();

})

function clearAllFields() //this wil clear all fields of last row
{
    var lastRow = document.getElementById('myTable').tFoot.children[0];
    lastRow.children[0].children[0].value = ''
    lastRow.children[1].children[0].selectedIndex = 0
    lastRow.children[2].children[0].value = ''
    lastRow.children[3].innerText = ''
}


/*
    This function will get values from last row and add row to table dynamically
*/
function addToTable() {
    var lastRow = document.getElementById('myTable').tFoot.children[0];
    var itemName = lastRow.children[0].children[0].value;
    var itemType = lastRow.children[1].children[0].value
    var dueDate = lastRow.children[2].children[0].value
    var condition = lastRow.children[3].innerText
    var todayDate = new Date();
    todayDate = todayDate.getFullYear() + '-' + (todayDate.getMonth() + 1) + '-' + todayDate.getDate()

    if (itemName == '' || itemType == '--' || dueDate == '' || condition == '') {
        console.log(itemName, itemType, dueDate, condition)
        alert('Fill all required fields')
    } else {
        dueDate = lastRow.children[2].children[0].value
        dueDate = new Date(dueDate)
        if (dueDate < todayDate) {
            alert('Select correct Due Date')
            lastRow.children[2].children[0].value = ''
        } else {
            document.getElementById('myTable').insertAdjacentHTML("afterbegin", `<tr>
            <td>
                ${lastRow.children[0].children[0].value}   
            </td>
            <td>
                ${lastRow.children[1].children[0].value}    
            </td>
            <td>
                ${lastRow.children[2].children[0].value}    
            </td>
            <td>
                ${lastRow.children[3].innerText}           
            </td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="removeRow(this)">Delete</button>
            </td>
        </tr>

        `);
            clearAllFields();

        }


    }

}