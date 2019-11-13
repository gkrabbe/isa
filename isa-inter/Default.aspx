<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="isa_inter.Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<!DOCTYPE html>

<head>
    <link rel="stylesheet" type="text/css" href="main.css">
</head>

<body>
    <img src ="a.png" id="image"/>
    <div class="init" id="sala1">ESTOU NA SALA1</div>
    <div class="init" id="sala2">ESTOU NA SALA2</div>
    <div class="init" id="cozinha">ESTOU NA COZINHA</div>
    <div class="init" id="quarto1">ESTOU NO QUARTO1</div>
    <div class="init" id="quarto2">ESTOU NO QUARTO2</div>
    <div class="init" id="fora">ESTOU FORA DE CASA</div>
    <div class="init" id="corredor">ESTOU NO CORREDOR</div>
    <div class="init" id="banheiro">BANHEIRO</div>
    <div class="init" id="servico">SERVICO</div>
    <div id="boxes">
      <form>

    <input type="radio" name="local" id='csala1' ></input> SALA1<br>
    <input type="radio" name="local" id='csala2' ></input> SALA2<br>
    <input type="radio" name="local" id='ccozinha' ></input> COZINHA<br>
    <input type="radio" name="local" disabled="disabled" id='cquarto1' ></input> QUARTO1<br>
    <input type="radio" name="local" id='cquarto2' ></input> QUARTO2<br>
    <input type="radio" name="local" id='ccorredor' ></input> CORREDOR<br>
    <input type="radio" name="local" id='cbanheiro' ></input> BANHEIRO<br>
    <input type="radio" name="local" id='cfora' ></input> FORA DE CASA<br>
    <input type="radio" name="local" id='cservico' ></input>AREA DE SERVICO<br>

    <script src="Scripts/jquery-1.6.4.min.js"></script>
    <script src="Scripts/jquery.signalR-2.4.1.js"></script>
    <script src="http://127.0.0.1:8088/signalr/hubs"></script>

   <script type="text/javascript">
       function myFunction() {

       }
       $(function () {
           $.connection.hub.url = "http://127.0.0.1:8088/signalr"
           var chat = $.connection.isaHub;

           chat.client.statusLocalization = function (name, is) {
               console.log(name, is, typeof is);
               document.getElementById(name).checked = is;
           };

           chat.client.statusLamp = function (name, is) {
               if (is == true) {
                   document.getElementById(name).style.display = "block";
               } else {
                   document.getElementById(name).style.display = "none";
               }
           };

            $.connection.hub.start().done(function () {                
                $('input').click(function () {

                    console.log($(this)[0]);
                    chat.server.sendlocalization($(this)[0].id, $(this)[0].checked);

                });
            });
        });
    </script>

</form>
    </div>
</body>

</html>
