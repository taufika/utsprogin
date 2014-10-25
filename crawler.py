from bs4 import BeautifulSoup					#melakukan import library beautifulsoup
import urllib							#melakukan import library urllib
import sys							#melakukan import library sys

baseurl = []							#inisialisasi list untuk baseurl
waitinglist = []						#inisialisasi list untuk waitinglist halaman yang akan diparse

def parsing(cururl, index):					#pendefinisian fungsi parsing
	print str(index) + ': Retrieving from ' + cururl	#mencetak url yang sedang akan dilakukan get
	with open('indexed/indexed.txt', 'r') as indexedf:	#membuka file indexed.txt untuk membaca daftar url yang pernah diparse
		indexed = indexedf.read().split('\n')		#mengassign isi file menjadi list bernama indexed
		lastnum = len(indexed)				#ukuran dari indexed
		urlarray = indexed				#memasukkan indexed ke list baru bernama urlarray

	if cururl != '' and cururl not in indexed:		#menentukan apakah url parameter sudah ada di list url yang pernah diparse
		response = urllib.urlopen(cururl)		#bila tidak dilakukan urlopen kepada url tersebut
		
		if response.info()['content-type'].startswith('text/html'):	#jika header dari response berisikan text/html
			print cururl + " is HTML"				#melakukan cetak ke layar konfirmasi hasil = html
			myhtml = BeautifulSoup(response.read())			#memasukkan hasil baca urlopen ke variable
			with open('indexed/'+str(lastnum-1)+'.html', 'w') as thefile:	#membuat file baru bernama nomor sebesar lastnum-1
				thefile.write(str(myhtml))				#mengisikan file dengan hasil retrieve html
			theurl = ''							#inisialisasi url untuk disimpan di list
		
			with open('indexed/indexed.txt', 'a') as indexedf:	#membuka file indexed.txt untuk menambahkan entry baru
				indexedf.write(cururl+'\n')			#menambahkan entry baru
				print cururl+' indexed!'			#mencetak pemberitahuan bahwa url telah diindekskan

			anchorlist = myhtml.find_all('a')			#membuat list berisikan seluruh tag anchor ( <a   > </a> )
			print str(len(anchorlist)) + ' Links found'		#menampilkan jumlah anchor yang didapat dari hasil retrieve
			for anchor in anchorlist:				#melakukan iterasi terhadap list anchor
				addurl = anchor.get('href')			#mengambil atribut href dari anchor ke variabel
				if str(addurl) == 'None' or  str(addurl).split('#')[0] == '':	#mengidentifikasi apakah url dari href kosong atau berupa anchor point (#)
					addurl = ''						#jika ya variable diisi string kosong
				if (str(addurl).split('/')[0].find('http') < 0) :	#mengidentifikasi apakah url dimulai dengan http://
					if (str(addurl).split('/')[0] == '') :		#jika tidak, apakah url absolute path (/path/)
						theurl = baseurl[-1]+addurl		#jika ya maka membuat url berdasarkan base+add
					else :						
						theurl = cururl+addurl			#jika tidak, membuat url relatif curr+add
						if addurl.split('?')[0] == '' :		#namun, jika addurl hanya berupa query
							theurl = cururl.split('?')[0] + addurl	#curr. url dihilangkan dulu querynya
					baseurl.append(baseurl[-1])			#menambahkan baseurl yang sekarang ke list baseurl
				else :						#jika addurl diawali dengan http://
					theurl = addurl				#url disamakan dengan addurl
					baseurl.append(theurl)			#url dipush ke dalam list baseurl

				if (theurl not in urlarray) and (cururl+'/' != theurl) :	#mengecek apakah url sudah ada di list url yang pernah diparse
					waitinglist.append(theurl)		#jika tidak, url kemudian dimasukkan ke waitinglist
					baseurl.pop()				#melakukan pop baseurl yang sudah digunakan
		else :
			print "Not HTML"				#jika hasil retrieve bukan html, menampilkan pesan
	else : 	
		print cururl + ' already indexed'			#jika url sudah ada di list, menampilkan pesan

				

def searchengine(param) :						#pendefinisian fungsi pencarian
	with open('indexed/indexed.txt', 'r') as indexedf:		#membuka file indexed.txt sebagai daftar url
		indexed = indexedf.read().split('\n')			#memasukkan isi file ke dalam list
		lastnum = len(indexed)-1				#nomor url terakhir yang ada dalam list
		
	searchresult = []						#inisialisasi list hasil pencarian
	print ('Searching')						#menampilkan pesan
	for i in range(0, lastnum) :						#mengiterasi seluruh isi dari list indexed
		with open('indexed/'+ str(i) +'.html', 'r') as htmlfile:	#membuka file dengan nama i .html
			content = BeautifulSoup(htmlfile.read()).body		#membaca isi file dan hanya diambil isi dari tag <body>
		invalid_tags = ['b', 'i', 'u', 'a', 'h1','h2','h3', 'div', 'strong']	#list tag yang akan dihilangkan tagnya
		
		if str(content) != 'None' :				#melihat apakah isi file kosong
			for tag in invalid_tags: 			#jika tidak kosong melakukan iterasi terhadap semua isi list invalid_tags
			    for match in content.findAll(tag):		#kemudian iterasi seluruh tag pada dokumen
				match.replaceWithChildren()		#seluruh tag yang cocok dengan invalid_tags dihilangkan tagnya (menjadi plain text)
		if str(content).find(param) != -1 :			#mencari keyword pada hasil perapihan sebelumnya
			searchresult.append(indexed[i])			#jika ditemukan url dimasukkan ke searchresult
			print str(len(searchresult)) + '. ' + searchresult[-1]	#menampilkan hasil ditemukan ke layar

	print '================================================='
	print 'Showing ' + str(len(searchresult)) + ' results'		#menampilkan jumlah page yang mengandung kata kunci
		
		

if len(sys.argv) > 2:						#membaca apakah program mendapat parameter yang cukup
	if (sys.argv[1] == '-crawl') :				#membaca apakah parameter 1 berisi -crawl
		url = sys.argv[2]				#jika ya maka dilihat parameter 2 sebagai url awal
		baseurl.append(url)				#memasukkan url ke baseurl
		waitinglist.append(url)				#memasukkan url ke waitinglist
		index = 0					#inisialisasi indeks
		while index < len(waitinglist) :		#melakukan iterasi hingga indeks >= panjang list waitinglist
			parsing(waitinglist[index], index)	#melakukan parsing terhadap url pada waitinglist
			index += 1				#menambah indeks

	elif (sys.argv[1] == '-search') :			#parameter 1 berisi -search
		print 'Searching for ' + sys.argv[2]		#menampilkan pesan apa kata kunci yang dicari
		print '================================================='
		searchengine(sys.argv[2])			#memanggil prosedur pencarian
	else :		
		print 'Correct use: crawler.py -search <term> or crawler.py -crawl <URL>'	#menampilkan pesan bahwa pengguna salah menggunakan program
else :
	print 'Error: Correct use: crawler.py -search <term> or crawler.py -crawl <URL> '	#menampilkan pesan bahwa pengguna salah menggunakan program

