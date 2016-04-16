// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://bbs.ustc.edu.cn/*
// @match        http://bbas.ustc.edu.cn/*
// @grant        none
// ==/UserScript==
/* jshint -W097 */
'use strict';

// Your code here...
var jq = document.createElement('script');
jq.src='https://code.jquery.com/jquery-2.1.4.min.js';
jq.type='text/javascript';
jq.onload = function(){
  main(window.jQuery);
}
document.head.appendChild(jq);

var top10 = 'https://bbs.ustc.edu.cn/cgi/bbstop10';
function main($){
  // load top10
  if(location.pathname == '/cgi/bbsindex') {// home page
      $.get('https://bbs.ustc.edu.cn/cgi/bbstop10', function(data){
          
          var tr = $(data).find('table tr');
          var vdata = []
          for(var i=1; i<tr.length; i++){
              var n = $(tr[i]);
              var name = n.find('td:first').text();
              var html = n.find('td:nth(2)').html();
              vdata.push({'name':name, 'html':html})
          }
          console.log(vdata);
          var td = $('<td class="topten">').append('<h3 class="label">今日十大<a class="more" title="查看十大" href="bbstop10">更多</a></h3>');
          var ul = $('<ul>');
          for(var i=0; i<vdata.length;i++){
              ul.append('<li><span>'+vdata[i].name+'</span>'+vdata[i].html+'</li>');
          }
          td.append(ul);
          $('.zones').remove();   //remove zone
          
          $('.notice').after(td);
          
          
          
      })
      
     
  }
}

