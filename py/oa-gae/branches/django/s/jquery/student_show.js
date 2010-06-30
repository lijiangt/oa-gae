 $j(document).ready(function(){
      $j("#student_show #s_left ul li:eq(0)").hover(
      function(){
          $j("#student_show #s_left ul li").each(function(){
          this.className="first";
          document.getElementById("s_right").className="s_right1";
          });
         $j("#content span").each(function(){
          this.style.display="none";
          }); 
          this.className="first";
          document.getElementById("s_right").className="s_right1";
          document.getElementById("c1").style.display="";
          document.getElementById("s_rt").style.cssText="margin-top:-300px;margin-left:630px;white-space:nowrap;";
        });
      
      $j("#student_show #s_left ul li:eq(1)").hover(
      function(){
         $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
      }); 
        $j("#content span").each(function(){
         this.style.display="none";
         }); 
         this.className="sencond";
         document.getElementById("s_right").className="s_right2";
         document.getElementById("c2").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-210px;margin-left:630px;white-space:nowrap;";
       });
       
       $j("#student_show #s_left ul li:eq(2)").hover(
        function(){
       $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
       }); 
      $j("#content span").each(function(){
         this.style.display="none";
         }); 
         this.className="third";
         document.getElementById("s_right").className="s_right3";
         document.getElementById("c3").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-240px;margin-left:630px;white-space:nowrap;";
       });
       
       
       $j("#student_show #s_left ul li:eq(3)").hover(
        function(){
        $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
      }); 
      $j("#content span").each(function(){
         this.style.display="none";
         }); 
         this.className="fourth";
         document.getElementById("s_right").className="s_right4";
         document.getElementById("c4").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-240px;margin-left:630px;white-space:nowrap;";
       });
       
       
       
       $j("#student_show #s_left ul li:eq(4)").hover(
        function(){
          $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
         }); 
        $j("#content span").each(function(){
         this.style.display="none";
         }); 
         this.className="fifth";
         document.getElementById("s_right").className="s_right5";
         document.getElementById("c5").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-180px;margin-left:630px;white-space:nowrap;";
       });
       
       
       $j("#student_show #s_left ul li:eq(5)").hover(
        function(){
         $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
        }); 
        $j("#content span").each(function(){
         this.style.display="none";
         }); 
         this.className="sixth";
         document.getElementById("s_right").className="s_right6";
         document.getElementById("c6").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-180px;margin-left:630px;white-space:nowrap;";
       });
       
       
       $j("#student_show #s_left ul li:eq(6)").hover(
        function(){
         $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
        }); 
        $j("#content span").each(function(){
         this.style.display="none";
        }); 
         this.className="seventh";
         document.getElementById("s_right").className="s_right7";
         document.getElementById("c7").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-150px;margin-left:630px;white-space:nowrap;";
       });
       
       
       $j("#student_show #s_left ul li:eq(7)").hover(
         function(){
         $j("#student_show #s_left ul li").each(function(){
         this.className="first";
         document.getElementById("s_right").className="s_right1";
        }); 
         $j("#content span").each(function(){
           this.style.display="none";
         }); 
         this.className="eighth";
         document.getElementById("s_right").className="s_right8";
         document.getElementById("c8").style.display="";
         document.getElementById("s_rt").style.cssText="margin-top:-150px;margin-left:630px;white-space:nowrap;";
       });
   });