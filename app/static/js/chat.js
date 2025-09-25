let socket;
let currentRoom = null;
let currentGroupCode = null;

function hideSidebar() {
	const sidebar = document.getElementById('sidebarCol');
	const backBtn = document.getElementById('backBtn');
	if (!sidebar || !backBtn) return;
	sidebar.classList.add('hidden-sidebar');
	sidebar.style.opacity = '0';
	backBtn.classList.remove('d-none');
}

function showSidebar() {
	const sidebar = document.getElementById('sidebarCol');
	const backBtn = document.getElementById('backBtn');
	if (!sidebar || !backBtn) return;
	sidebar.classList.remove('hidden-sidebar');
	sidebar.style.opacity = '1';
	backBtn.classList.add('d-none');
	setOnlineCount(null);
}

function leaveCurrent() {
	if (socket) {
		const payload = currentGroupCode ? { code: currentGroupCode } : { room: currentRoom, region: window.region };
		socket.emit('leave', payload);
	}
	currentRoom = null;
	currentGroupCode = null;
	showSidebar();
	document.getElementById('roomName').innerText = 'None';
	document.getElementById('messages').innerHTML = '';
}

function setOnlineCount(count) {
	const badge = document.getElementById('onlineBadge');
	const num = document.getElementById('onlineCount');
	if (!badge || !num) return;
	if (count === null || count === undefined || count <= 0) {
		badge.classList.add('d-none');
		num.textContent = '0';
		return;
	}
	num.textContent = String(count);
	badge.classList.remove('d-none');
}

function joinRoom(roomName) {
	currentGroupCode = null;
	connectSocketIfNeeded();
	currentRoom = roomName;
	document.getElementById('roomName').innerText = roomName;
	document.getElementById('messages').innerHTML = '';
	hideSidebar();
	socket.emit('join', { room: roomName, region: window.region, nickname: window.nickname });
}

function joinByCode(code) {
	currentRoom = null;
	currentGroupCode = (code || '').toUpperCase();
	if (!currentGroupCode) return;
	connectSocketIfNeeded();
	document.getElementById('roomName').innerText = `Room ${currentGroupCode}`;
	document.getElementById('messages').innerHTML = '';
	hideSidebar();
	socket.emit('join', { code: currentGroupCode, region: window.region, nickname: window.nickname });
}

function connectSocketIfNeeded() {
	if (!socket) {
		socket = io();
		socket.on('status', (data) => {
			appendStatus(data.message);
		});
		socket.on('typing', (data) => {
			document.getElementById('typing').innerText = `${data.nickname} is typing...`;
			setTimeout(() => (document.getElementById('typing').innerText = ''), 1200);
		});
		socket.on('message', (data) => {
			appendMessage(`${data.nickname}: ${data.text}`);
		});
		socket.on('presence', (data) => {
			setOnlineCount(data.count);
		});
		document.getElementById('messageInput').addEventListener('keydown', (e) => {
			if (e.key === 'Enter' && !e.shiftKey) {
				e.preventDefault();
				sendMessage();
			}
		});
		document.getElementById('messageInput').addEventListener('input', () => {
			if (!currentRoom && !currentGroupCode) return;
			const payload = currentGroupCode ? { code: currentGroupCode } : { room: currentRoom, region: window.region };
			socket.emit('typing', { ...payload, region: window.region, nickname: window.nickname });
		});
	}
}

function sendMessage() {
	const input = document.getElementById('messageInput');
	const text = input.value.trim();
	if (!text || (!currentRoom && !currentGroupCode)) return;
	const payload = currentGroupCode ? { code: currentGroupCode } : { room: currentRoom, region: window.region };
	socket.emit('message', { ...payload, region: window.region, nickname: window.nickname, text });
	input.value = '';
}

function insertEmoji(emoji) {
	const input = document.getElementById('messageInput');
	const start = input.selectionStart || input.value.length;
	const end = input.selectionEnd || input.value.length;
	input.value = input.value.slice(0, start) + emoji + input.value.slice(end);
	input.focus();
	const caret = start + emoji.length;
	input.setSelectionRange(caret, caret);
}

function appendMessage(text) {
	const div = document.createElement('div');
	div.className = 'fade-in';
	div.textContent = text;
	document.getElementById('messages').appendChild(div);
	document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
}

function appendStatus(text) {
	const div = document.createElement('div');
	div.className = 'text-muted small fade-in';
	div.textContent = text;
	document.getElementById('messages').appendChild(div);
}

window.joinRoom = joinRoom;
window.joinByCode = joinByCode;
window.sendMessage = sendMessage;
window.insertEmoji = insertEmoji;
window.leaveCurrent = leaveCurrent;
