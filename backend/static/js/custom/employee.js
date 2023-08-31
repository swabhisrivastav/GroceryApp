var employeeModal = $("#employeeModal");
    $(function () {

        //JSON data by API call
        $.get(employeeListApiUrl, function (response) {
            if(response) {
                var table = '';
                $.each(response, function(index, employee) {
                    table += '<tr data-id="'+ employee.employee_id +'" data-first_name="'+ employee.first_name   + '" data-last_name="'+ employee.last_name +'" data-designation="'+ employee.designation +'" data-date_of_joining="'+ employee.date_of_joining +'">' +
                        '<td>'+ employee.first_name +'</td>'+
                        '<td>'+ employee.last_name +'</td>'+
                        '<td>'+ employee.designation +'</td>'+
                        '<td>'+ employee.date_of_joining +'</td>'+
                        '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });

    // Save Employee
    $("#saveEmployee").on("click", function () {
        // If we found id value in form then update employee detail
        var data = $("#employeeForm").serializeArray();
        var requestPayload = {
            first_name: null,
            last_name: null,
            designation: null,
            date_of_joining: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'first_name':
                    requestPayload.first_name = element.value;
                    break;
                case 'last_name':
                    requestPayload.last_name = element.value;
                    break;
                case 'designation':
                    requestPayload.designation = element.value;
                    break;
                case 'date_of_joining':
                    requestPayload.date_of_joining = element.value;
                    break;  
            }
        }
        callApi("POST", employeeSaveApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            employee_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('first_name') );
        if (isDelete) {
            callApi("POST", employeeDeleteApiUrl, data);
        }
    });

    employeeModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#first_name, #last_name, #designation, #date_of_joining").val('');
        employeeModal.find('.modal-title').text('Add New Employee');
    });

    
   