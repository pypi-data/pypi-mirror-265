import{p,g as O,c as u,l,af as G,aP as le,aM as Y,b1 as Z,d as re,e as ue,u as de,as as ce,r as B,t as fe,w as ve,a as me,F as E,n as N,b2 as ge,b3 as ye,h as be,aL as xe,ae as Ce,b4 as Ve,q as Q,b5 as he}from"./index-2ed92f93.js";import{a as H,I as ke,Z as _e,i as U,M as Ie,W as Pe,c as Fe,P as Se,g as Be,e as we,J as Re,_ as Te,L as Le,R as $e,$ as Ae,N as Me,a0 as De,F as Ee}from"./forwardRefs-b2545869.js";import{f as Ne,g as pe,u as te,k as Oe,m as Ue,b as ee}from"./VCheckboxBtn-f2c5d38b.js";const We=p({active:Boolean,max:[Number,String],value:{type:[Number,String],default:0},...H(),...ke({transition:{component:_e}})},"VCounter"),je=O()({name:"VCounter",functional:!0,props:We(),setup(e,y){let{slots:a}=y;const h=u(()=>e.max?`${e.value} / ${e.max}`:String(e.value));return U(()=>l(Ie,{transition:e.transition},{default:()=>[G(l("div",{class:["v-counter",e.class],style:e.style},[a.default?a.default({counter:h.value,max:e.max,value:e.value}):h.value]),[[le,e.active]])]})),{}}});const qe=p({floating:Boolean,...H()},"VFieldLabel"),D=O()({name:"VFieldLabel",props:qe(),setup(e,y){let{slots:a}=y;return U(()=>l(Ne,{class:["v-field-label",{"v-field-label--floating":e.floating},e.class],style:e.style,"aria-hidden":e.floating||void 0},a)),{}}}),ze=["underlined","outlined","filled","solo","solo-inverted","solo-filled","plain"],ne=p({appendInnerIcon:Y,bgColor:String,clearable:Boolean,clearIcon:{type:Y,default:"$clear"},active:Boolean,centerAffix:{type:Boolean,default:void 0},color:String,baseColor:String,dirty:Boolean,disabled:{type:Boolean,default:null},error:Boolean,flat:Boolean,label:String,persistentClear:Boolean,prependInnerIcon:Y,reverse:Boolean,singleLine:Boolean,variant:{type:String,default:"filled",validator:e=>ze.includes(e)},"onClick:clear":Z(),"onClick:appendInner":Z(),"onClick:prependInner":Z(),...H(),...Pe(),...Fe(),...re()},"VField"),ae=O()({name:"VField",inheritAttrs:!1,props:{id:String,...pe(),...ne()},emits:{"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,y){let{attrs:a,emit:h,slots:t}=y;const{themeClasses:b}=ue(e),{loaderClasses:C}=Se(e),{focusClasses:W,isFocused:w,focus:R,blur:T}=te(e),{InputIcon:k}=Oe(e),{roundedClasses:j}=Be(e),{rtlClasses:L}=de(),V=u(()=>e.dirty||e.active),f=u(()=>!e.singleLine&&!!(e.label||t.label)),q=ce(),o=u(()=>e.id||`input-${q}`),z=u(()=>`${o.value}-messages`),$=B(),_=B(),A=B(),n=u(()=>["plain","underlined"].includes(e.variant)),{backgroundColorClasses:d,backgroundColorStyles:c}=we(fe(e,"bgColor")),{textColorClasses:v,textColorStyles:J}=Re(u(()=>e.error||e.disabled?void 0:V.value&&w.value?e.color:e.baseColor));ve(V,s=>{if(f.value){const i=$.value.$el,m=_.value.$el;requestAnimationFrame(()=>{const g=Te(i),r=m.getBoundingClientRect(),P=r.x-g.x,F=r.y-g.y-(g.height/2-r.height/2),x=r.width/.75,S=Math.abs(x-g.width)>1?{maxWidth:me(x)}:void 0,M=getComputedStyle(i),K=getComputedStyle(m),ie=parseFloat(M.transitionDuration)*1e3||150,oe=parseFloat(K.getPropertyValue("--v-field-label-scale")),se=K.getPropertyValue("color");i.style.visibility="visible",m.style.visibility="hidden",Le(i,{transform:`translate(${P}px, ${F}px) scale(${oe})`,color:se,...S},{duration:ie,easing:Me,direction:s?"normal":"reverse"}).finished.then(()=>{i.style.removeProperty("visibility"),m.style.removeProperty("visibility")})})}},{flush:"post"});const I=u(()=>({isActive:V,isFocused:w,controlRef:A,blur:T,focus:R}));function X(s){s.target!==document.activeElement&&s.preventDefault()}return U(()=>{var P,F,x;const s=e.variant==="outlined",i=!!(t["prepend-inner"]||e.prependInnerIcon),m=!!(e.clearable||t.clear),g=!!(t["append-inner"]||e.appendInnerIcon||m),r=()=>t.label?t.label({...I.value,label:e.label,props:{for:o.value}}):e.label;return l("div",N({class:["v-field",{"v-field--active":V.value,"v-field--appended":g,"v-field--center-affix":e.centerAffix??!n.value,"v-field--disabled":e.disabled,"v-field--dirty":e.dirty,"v-field--error":e.error,"v-field--flat":e.flat,"v-field--has-background":!!e.bgColor,"v-field--persistent-clear":e.persistentClear,"v-field--prepended":i,"v-field--reverse":e.reverse,"v-field--single-line":e.singleLine,"v-field--no-label":!r(),[`v-field--variant-${e.variant}`]:!0},b.value,d.value,W.value,C.value,j.value,L.value,e.class],style:[c.value,e.style],onClick:X},a),[l("div",{class:"v-field__overlay"},null),l($e,{name:"v-field",active:!!e.loading,color:e.error?"error":typeof e.loading=="string"?e.loading:e.color},{default:t.loader}),i&&l("div",{key:"prepend",class:"v-field__prepend-inner"},[e.prependInnerIcon&&l(k,{key:"prepend-icon",name:"prependInner"},null),(P=t["prepend-inner"])==null?void 0:P.call(t,I.value)]),l("div",{class:"v-field__field","data-no-activator":""},[["filled","solo","solo-inverted","solo-filled"].includes(e.variant)&&f.value&&l(D,{key:"floating-label",ref:_,class:[v.value],floating:!0,for:o.value,style:J.value},{default:()=>[r()]}),l(D,{ref:$,for:o.value},{default:()=>[r()]}),(F=t.default)==null?void 0:F.call(t,{...I.value,props:{id:o.value,class:"v-field__input","aria-describedby":z.value},focus:R,blur:T})]),m&&l(Ae,{key:"clear"},{default:()=>[G(l("div",{class:"v-field__clearable",onMousedown:S=>{S.preventDefault(),S.stopPropagation()}},[t.clear?t.clear():l(k,{name:"clear"},null)]),[[le,e.dirty]])]}),g&&l("div",{key:"append",class:"v-field__append-inner"},[(x=t["append-inner"])==null?void 0:x.call(t,I.value),e.appendInnerIcon&&l(k,{key:"append-icon",name:"appendInner"},null)]),l("div",{class:["v-field__outline",v.value],style:J.value},[s&&l(E,null,[l("div",{class:"v-field__outline__start"},null),f.value&&l("div",{class:"v-field__outline__notch"},[l(D,{ref:_,floating:!0,for:o.value},{default:()=>[r()]})]),l("div",{class:"v-field__outline__end"},null)]),n.value&&f.value&&l(D,{ref:_,floating:!0,for:o.value},{default:()=>[r()]})])])}),{controlRef:A}}});function Je(e){const y=Object.keys(ae.props).filter(a=>!ge(a)&&a!=="class"&&a!=="style");return ye(e,y)}const Xe=["color","file","time","date","datetime-local","week","month"],Ye=p({autofocus:Boolean,counter:[Boolean,Number,String],counterValue:[Number,Function],prefix:String,placeholder:String,persistentPlaceholder:Boolean,persistentCounter:Boolean,suffix:String,role:String,type:{type:String,default:"text"},modelModifiers:Object,...Ue(),...ne()},"VTextField"),Ke=O()({name:"VTextField",directives:{Intersect:De},inheritAttrs:!1,props:Ye(),emits:{"click:control":e=>!0,"mousedown:control":e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,y){let{attrs:a,emit:h,slots:t}=y;const b=be(e,"modelValue"),{isFocused:C,focus:W,blur:w}=te(e),R=u(()=>typeof e.counterValue=="function"?e.counterValue(b.value):typeof e.counterValue=="number"?e.counterValue:(b.value??"").toString().length),T=u(()=>{if(a.maxlength)return a.maxlength;if(!(!e.counter||typeof e.counter!="number"&&typeof e.counter!="string"))return e.counter}),k=u(()=>["plain","underlined"].includes(e.variant));function j(n,d){var c,v;!e.autofocus||!n||(v=(c=d[0].target)==null?void 0:c.focus)==null||v.call(c)}const L=B(),V=B(),f=B(),q=u(()=>Xe.includes(e.type)||e.persistentPlaceholder||C.value||e.active);function o(){var n;f.value!==document.activeElement&&((n=f.value)==null||n.focus()),C.value||W()}function z(n){h("mousedown:control",n),n.target!==f.value&&(o(),n.preventDefault())}function $(n){o(),h("click:control",n)}function _(n){n.stopPropagation(),o(),Q(()=>{b.value=null,he(e["onClick:clear"],n)})}function A(n){var c;const d=n.target;if(b.value=d.value,(c=e.modelModifiers)!=null&&c.trim&&["text","search","password","tel","url"].includes(e.type)){const v=[d.selectionStart,d.selectionEnd];Q(()=>{d.selectionStart=v[0],d.selectionEnd=v[1]})}}return U(()=>{const n=!!(t.counter||e.counter!==!1&&e.counter!=null),d=!!(n||t.details),[c,v]=xe(a),{modelValue:J,...I}=ee.filterProps(e),X=Je(e);return l(ee,N({ref:L,modelValue:b.value,"onUpdate:modelValue":s=>b.value=s,class:["v-text-field",{"v-text-field--prefixed":e.prefix,"v-text-field--suffixed":e.suffix,"v-input--plain-underlined":k.value},e.class],style:e.style},c,I,{centerAffix:!k.value,focused:C.value}),{...t,default:s=>{let{id:i,isDisabled:m,isDirty:g,isReadonly:r,isValid:P}=s;return l(ae,N({ref:V,onMousedown:z,onClick:$,"onClick:clear":_,"onClick:prependInner":e["onClick:prependInner"],"onClick:appendInner":e["onClick:appendInner"],role:e.role},X,{id:i.value,active:q.value||g.value,dirty:g.value||e.dirty,disabled:m.value,focused:C.value,error:P.value===!1}),{...t,default:F=>{let{props:{class:x,...S}}=F;const M=G(l("input",N({ref:f,value:b.value,onInput:A,autofocus:e.autofocus,readonly:r.value,disabled:m.value,name:e.name,placeholder:e.placeholder,size:1,type:e.type,onFocus:o,onBlur:w},S,v),null),[[Ce("intersect"),{handler:j},null,{once:!0}]]);return l(E,null,[e.prefix&&l("span",{class:"v-text-field__prefix"},[l("span",{class:"v-text-field__prefix__text"},[e.prefix])]),t.default?l("div",{class:x,"data-no-activator":""},[t.default(),M]):Ve(M,{class:x}),e.suffix&&l("span",{class:"v-text-field__suffix"},[l("span",{class:"v-text-field__suffix__text"},[e.suffix])])])}})},details:d?s=>{var i;return l(E,null,[(i=t.details)==null?void 0:i.call(t,s),n&&l(E,null,[l("span",null,null),l(je,{active:e.persistentCounter||C.value,value:R.value,max:T.value},t.counter)])])}:void 0})}),Ee({},L,V,f)}});export{Ke as V,Ye as m};
