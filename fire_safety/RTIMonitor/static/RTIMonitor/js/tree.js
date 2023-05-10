var groups = document.getElementsByClassName("group");
for (var i = 0; i<groups.length; i++){
	groups[i].addEventListener(
		'click', function() {
			this.parentElement.nextElementSibling.classList.toggle('active');
			this.classList.toggle('active');
			this.children[0].classList.toggle('fa-folder');
			this.children[0].classList.toggle('fa-folder-open');
		});
}