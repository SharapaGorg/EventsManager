(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{295:function(t,e,r){"use strict";var n=r(2),o=r(301);n({target:"String",proto:!0,forced:r(302)("link")},{link:function(t){return o(this,"a","href",t)}})},301:function(t,e,r){var n=r(5),o=r(24),c=r(13),d=/"/g,l=n("".replace);t.exports=function(t,e,r,n){var v=c(o(t)),m="<"+e;return""!==r&&(m+=" "+r+'="'+l(c(n),d,"&quot;")+'"'),m+">"+v+"</"+e+">"}},302:function(t,e,r){var n=r(3);t.exports=function(t){return n((function(){var e=""[t]('"');return e!==e.toLowerCase()||e.split('"').length>3}))}},321:function(t,e,r){var content=r(334);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(65).default)("e1c58522",content,!0,{sourceMap:!1})},333:function(t,e,r){"use strict";r(321)},334:function(t,e,r){var n=r(64)((function(i){return i[1]}));n.push([t.i,".event-card[data-v-5c37c052]{margin-left:auto;margin-right:auto;width:33.333333%;border-radius:0.375rem;--tw-bg-opacity:1;background-color:rgb(35 39 42 / var(--tw-bg-opacity));--tw-text-opacity:1;color:rgb(225 223 223 / var(--tw-text-opacity));position:relative;top:70px;padding-left:1.25rem;padding-right:1.25rem;padding-top:1.25rem;padding-bottom:1.25rem}.event-card .title[data-v-5c37c052]{text-align:center;font-size:1.25rem;line-height:1.75rem;font-weight:700}.division-line[data-v-5c37c052]{margin-left:auto;margin-right:auto;margin-top:0.25rem;margin-bottom:0.25rem;width:90%;border-bottom-width:2px;--tw-border-opacity:1;border-color:rgb(225 223 223 / var(--tw-border-opacity))}.event-card .description[data-v-5c37c052]{margin-left:1rem;margin-right:1rem;max-height:400px;padding-top:0.25rem;padding-bottom:0.25rem;text-align:justify;overflow-y:auto}.event-card .link[data-v-5c37c052]{margin-left:2.5rem;display:inline;font-weight:700}.event-card a[data-v-5c37c052]{--tw-text-opacity:1;color:rgb(59 130 246 / var(--tw-text-opacity))}",""]),n.locals={},t.exports=n},338:function(t,e,r){"use strict";r.r(e);r(30),r(48),r(295);var n=r(9),o=(r(47),{data:function(){return{event:{},start:"",finish:"",defaultDesc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."}},mounted:function(){var t=this;return Object(n.a)(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=t.$route.params,e.next=3,t.$axios.$post(t.url+"event",{id:r.id});case 3:t.event=e.sent,t.start=new Date(1e3*t.event.start),t.finish=new Date(1e3*t.event.finish);case 6:case"end":return e.stop()}}),e)})))()},computed:{url:function(){return this.$store.state.url}}}),c=(r(333),r(46)),component=Object(c.a)(o,(function(){var t=this,e=t._self._c;return e("div",{staticClass:"event-card"},[e("div",{staticClass:"title"},[t._v(t._s(t.event.title))]),t._v(" "),e("div",{staticClass:"division-line"}),t._v(" "),e("div",{staticClass:"description"},[t._v(t._s(t.event.description))]),t._v(" "),e("div",{staticClass:"division-line"}),t._v(" "),e("div",{staticClass:"link"},[t._v("Ссылка:")]),t._v(" "),e("a",{attrs:{href:t.event.link}},[t._v(t._s(t.event.link))]),t._v(" "),e("div",[t._v(t._s(t.start))]),t._v(" "),e("div",[t._v(t._s(t.finish))])])}),[],!1,null,"5c37c052",null);e.default=component.exports}}]);