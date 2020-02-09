function submit_message(message) 
{
        $.post( "/send_message", {message: message}, handle_response);
        
        function handle_response(data) 
        {
          
            // remove the loading indicator
            $( "#loading" ).remove();

            // append the bot repsonse to the div
            if(data.type=="default")
            {
                $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${data.message}
                </div>
                `)
            }
            else
            {
                if (data.message[0][0].type=="placement")
                {
                    for (var i = 1; i < data.message.length ; i++) 
                    {
                        $('.chat-container').append(`
                        <div class="chat-message col-md-5 offset-md-7 bot-message">
                        ${data.message[i].company} : ${data.message[i].number}<br/>
                        
                        </div> `)    
                    }
                    
                }
                else if (data.message[0][0].type=="printForm") 
                {

                    $('.chat-container').append(`
                    <div class="chat-message col-md-5 offset-md-7 bot-message">
                    Provide Payment
                    </div> `)

                    popup('/processPayment?myparam1=2','Payment',700,400);
                }
                else if (data.message[0][0].type=="notFound") 
                {
                    for (var i = 1; i < data.message.length ; i++) 
                    {
                        $('.chat-container').append(`
                        <div class="chat-message col-md-5 offset-md-7 bot-message">
                        ${data.message[i].details}
                        </div> `)
                    }
                    
                }
            }
            var objDiv = document.getElementById("chat-window");
            objDiv.scrollTop = objDiv.scrollHeight;
         
          
          

           
        }



}
 
 $('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
          return
        }

        $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

        // loading 
        $('.chat-container').append(`
            <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
                Please wait<b>...</b>
            </div>
        `)
        var objDiv = document.getElementById("chat-window");
        objDiv.scrollTop = objDiv.scrollHeight;

        // clear the text input 
        $('#input_message').val('')

        // send the message
        submit_message(input_message)

    });

function popup(url, title, width, height) { 
    var left = (screen.width / 2) - (width / 2);
    var top = (screen.height / 2) - (height / 2);
    var options = '';
    options += ',width=' + width; 
    options += ',height=' + height; options += ',top=' + top; options += ',left=' + left; 
    return window.open(url, title, options); 
} 
function setData(data) {       
  window.paymentDatas=data;
  console.log(data);
   $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${window.paymentDatas}
                </div>
          `)
}

