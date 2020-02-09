

$('#popupForm').submit(function(e) {    
     e.preventDefault();        
     $.ajax({             
      	url: '/pay', 	    
      	data:$(this).serializeArray()        
      	}).then(function(data) {   
      	           console.log(JSON.stringify(data)); 
      	           window.opener.setData(data);       
      	           window.close();        
      	        });    
 });     