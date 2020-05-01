<script>
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelector('#register').disabled = true;
    
            document.querySelector('#username').onchange = () => {
                if (document.querySelector('#username').value.length > 0 && document.querySelector('#username').value.include('@')) {
                //             pwd = document.querySelector('#password').value
                //             if (pwd.length > 6) {
                //                 var strongRegex = new RegExp("^(?=.[a-z])(?=.[A-Z])(?=.[0-9])(?=.[!@#\$%\^&\*])(?=.{8,})");
                //                 val = strongRegex.test(String(pwd))
                //                 if (val){
                    document.querySelector('#register').disabled = false;
                }
                else {
                    document.querySelector('#usernamedp').innerHTML = "should be in the form of abc@xy.zz"
                    document.querySelector('#register').disabled = false;
                }
                //                 else {
                //                     document.querySelector('#passwordp').innerHTML = " The password should have atleast 1 uppercase, 1 lowercase, 1 digit and 1 special char and length should be more than 6 "
                //                 }
                //             }
                //             else
                //                 document.querySelector('#register').disabled = true;
                //                 document.querySelector('#usernamedp').innerHTML = "should be in the form of abc@xy.zz"
                //         };
    
                //         document.querySelector('.form-group').onsubmit = () => {
    
                //         // Create new item for list
    
    
                //         // Add new item to task list
    
                //         // Clear input field and disable button again
                //         document.querySelector('#username').value = '';
                //         document.querySelector('#password').value = '';
                //         document.querySelector('#register').disabled = true;
    
                        // Stop form from submitting
            //             return false;
            //         }
            //     }
                //     document.querySelector('#register').disabled = false;
                // }
                
            };

        });
    </script>