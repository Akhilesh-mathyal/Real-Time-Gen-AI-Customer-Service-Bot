const chat = document.querySelector('#chat'), form = document.querySelector('#chatForm'), input = document.querySelector('#message'), send = document.querySelector('#send'), mode = document.querySelector('#mode');
const history = [];
function append(role, content = '') { const node = document.createElement('article'); node.className = `message ${role}`; node.textContent = content; chat.append(node); chat.scrollTop = chat.scrollHeight; return node; }
async function ask(message) {
  append('user', message); history.push({role:'user', content:message}); input.value=''; send.disabled=true; const answer=append('assistant');
  try { const response=await fetch('/api/chat/stream',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message,history:history.slice(0,-1)})}); if(!response.ok) throw new Error((await response.json()).error); const reader=response.body.getReader(), decoder=new TextDecoder(); let buffer='';
    while(true){const {done,value}=await reader.read();if(done)break;buffer+=decoder.decode(value,{stream:true});const chunks=buffer.split('\n\n');buffer=chunks.pop();for(const chunk of chunks){const event=(chunk.match(/^event: (.+)$/m)||[])[1], data=(chunk.match(/^data: (.+)$/m)||[])[1];if(!data)continue;const text=JSON.parse(data);if(event==='token'){answer.textContent+=text;chat.scrollTop=chat.scrollHeight}else if(event==='mode'){mode.textContent=text==='live'?'Live AI':'Demo mode'}else if(event==='error'){answer.textContent=text}}}
    history.push({role:'assistant',content:answer.textContent});
  }catch(error){answer.textContent=error.message||'Unable to send your message.';} finally {send.disabled=false;input.focus();}
}
form.onsubmit=e=>{e.preventDefault();const message=input.value.trim();if(message)ask(message)};document.querySelectorAll('.suggestions button').forEach(button=>button.onclick=()=>ask(button.textContent));document.querySelector('#handoff').onclick=()=>append('assistant','A human-support request has been noted. In production, connect this action to your help-desk ticketing system.');
