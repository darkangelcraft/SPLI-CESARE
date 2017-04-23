#!/usr/bin/ruby
#$KCODE = 'a'
ENCRYPTED_FILE="input.txt"
DECRYPTED_FILE="frequency_decrypted_text.txt"
FREQUENCIES_DICTIONARY_FILE="frequency_dictionary.txt"
WORDS_DICTIONARY_FILE="words_dictionary.txt"
PRECISION=200
THRESHOLD=0.6

BEGIN {
puts "\n\n\t|--------------------------------|"
puts "\t|Frequency Attack - Caesar Cipher|\n"
puts "\t|--------------------------------|\n\n"
}

#CONTROLLO ESISTENZA DIZIONARIO DELLE FREQUENZE
def dictionary_exist
	exist_f=File.exist?(FREQUENCIES_DICTIONARY_FILE)
	exist_w=File.exist?(WORDS_DICTIONARY_FILE)
	if(exist_f)
		puts"the frequency_dictionary file exists"
	else
		puts"the frequency_dictionary file doesn't exist"
	end
	if(exist_w)
		puts"the words_dictionary file exists"
	else
		puts"the words_dictionary file doesn't exist"
	end
	return (exist_w and exist_f)
end

#CREAZIONE DIZIONARIO FREQUENZE
def create_fdictionary
	f=File.new(FREQUENCIES_DICTIONARY_FILE,"w")
	tmp=nil
	Dir.foreach("testi/") do |fname|
 		if((fname.include? ".txt")==true)
 			tmp=File.read("testi/#{fname}")
 			f.puts "#{tmp.downcase} \n\n"
 		end
	end
	f.close
	puts"dictionary of frequencies created!"
end

#CREAZIONE DIZIONARIO FREQUENZE
def create_wdictionary
	tmp=""
	str=""
	array=[]
	flag=false
	Dir.foreach("testi/") do |fname|
 		if((fname.include? ".txt")==true)
 			tmp=File.read("testi/#{fname}")
 			str << tmp.downcase
 		end
	end
	#str contiene tutti i testi in append
	f=File.new(WORDS_DICTIONARY_FILE,"w")
	str.scan(/\w+/) {|word|
		flag=array.include?(word)
		if(!flag)
			f.puts word
			array << word
		end
		#scrivo sul file tutte le parole solo se non ripetute con un controllo su array
	}
	f.close
	puts"dictionary of words created!"
end

#CALCOLO DELLE FREQUENZE PER OGNI CARATTERE
def calculate_frequencies(target_file)
	n_char=0.0


	text=File.read(target_file)

	#creo l'hash delle lettere
	hsh=Hash.new
	code=97
	while code<=122 do
		hsh[code]=Occurrences.new(0,0.000)
		code+=1
	end
	#conto le occorrenze delle lettere
	text.each_byte {|c|
		if c>=97 and c<=122;
			hsh[c].number+=1
			n_char+=1
		end
	}
	#creo le frequenze
	hsh.each {|k, v|
		v[1]=v[0]/n_char
		#puts"number:#{v[0]} - percentage:#{v[1]}"
	}
	#print dei valori creati
	#i=0
	#hsh.each {|k, v| puts "elemento #{i} ---> #{k} is #{v}",
	#	i+=1
	#}
	return hsh;
end

#DECRIPTAZIONE TESTO CIFRATO
def decrypt(offset)
	char=''
	result=""
	str=File.read(ENCRYPTED_FILE)
	#caso offset positivo
	if (offset.to_i>0)
	str.each_byte {|c|
		if c>=97 and c<=122;
			if (c-offset)>=97 and (c-offset)<=122;
				char=(c-offset).chr
			else
				char=(123-(offset-(c-97))).chr
			end
		else
			char=c.chr
		end
		result<<char
		}
	#caso offset negativo
	elsif(offset.to_i<0)
		str.each_byte {|c|
		if c>=97 and c<=122;
			if (c-offset)>=97 and (c-offset)<=122;
				char=(c+offset).chr
			else
				char=(123-(offset-(c-97))).chr
			end
		else
			char=c.chr
		end
		result<<char
		}
	#caso offset=0
	else
		puts"the text is not encrypted, it's a clear text"
		result=str
	end
	return result
end

#CONTROLLO SULLA CORRETTEZZA DEL TESTO DECIFRATO
def corrected_decryption(decrypted_text)
	total_words=0.0
	n_matches=0
	matches_rate=0
	words_dictionary=File.read(WORDS_DICTIONARY_FILE)
	words_dictionary_array=words_dictionary.split(/\W+/)
	decrypted_words=decrypted_text.split(/\W+/)

	while(total_words<=PRECISION) do
		if(words_dictionary_array.include?(decrypted_words[total_words])==true)
			n_matches+=1
		end
		total_words+=1
	end
	if((n_matches/total_words)>=THRESHOLD)
		return true
	else
		return false
	end
end

#SEQUENZA DI OPERAZIONI NECESSARIE ALL'ATTACCO IN FREQUENZA
def frequency_attack(flag)
	if(flag==false)
		puts"you cannot make a frequency attack, one or more dictionaries missing!"
	else
		t1=Time.now
		t2=0
		time=0
		puts"\t---attack in progress---\n"
		i=0
		temp_offset=0
		decrypted_text=""
		a1=Array.new(26)
		a2=Array.new(26)
		possible_offsets=[]
		h3=Hash.new
		#calcolo frequenze per i due file
		h1=calculate_frequencies(ENCRYPTED_FILE)
		h2=calculate_frequencies(FREQUENCIES_DICTIONARY_FILE)
		#ordinamento hash sul campo delle occorenze
		h1=h1.sort_by {|_key, value| value[0]}.to_h
		h2=h2.sort_by {|_key, value| value[0]}.to_h
		#inserimento valore in array e inversione
		h1.each {|k, v| a1=a1.push(k)}
		h2.each {|k, v| a2=a2.push(k)}
		a1=a1.reverse
		a2=a2.reverse
		#calcolo possibili offset e del loro relativo punteggio
		while(i<26) do
			temp_offset=a1[i]-a2[i];
			#puts "\n\n=====================\ntemp_offset::#{temp_offset}"
			if (h3.has_key?(temp_offset)==true)
				h3[temp_offset]=h3[temp_offset]+1
			else
				h3[temp_offset]=1
			end
			#puts"iterazione numero:#{i}	-->#{a1[i]} - #{a2[i]}"
			i+=1
		end
		#ordinamento possibili offset per punteggio
		h3=h3.sort_by {|k, v| v}.to_h
		h3.each {|k, v| possible_offsets.unshift(k)}
		#tentativo di decriptazione per ogni offset con conseguente controllo sulla validità (dal più probabile al meno probabile)
		possible_offsets.each {|x|
			decrypted_text=decrypt(x);
			if(corrected_decryption(decrypted_text)==true)
				break
			end
		 }
		i=0
		print"\n\nsmall preview of the decrypted text\n\n"
		decrypted_text.each_line {|l|
			print l
			i+=1
			if(i>20)
				break
			end
		}
		f=File.new(DECRYPTED_FILE,"w")
 		f.puts "#{decrypted_text} \n\n";
		f.close
		t2=Time.now
		time=(t2-t1).round(3)
		puts"time spent:#{time} seconds"
		puts "\n==================================================================="
		puts "Attack finished! You can open and read frequency_decrypted_text.txt\n===================================================================\n\n\n"
	end
end

#=================================INIZIO "MAIN"=================================
#struttura per le occorrenze di una lettera
Occurrences = Struct.new(:number, :percentage) do
	def show
		"Content: #{number}, #{percentage}"
	end
end

selection=5
flag=false
while((selection.to_i)!=0)do
	puts"\tMAIN MENU"
	puts"\n1) dictionaries exist?"
	puts"2) create frequency_dictionary"
	puts"3) create words_dictionary"
	puts"4) make attack and exit"
	puts"5) exit"
	selection=gets.chomp
	puts case selection.to_i
	when 1
		flag=dictionary_exist
	when 2
		create_fdictionary
	when 3
		create_wdictionary
	when 4
		frequency_attack(flag)
		break
	when 5
		exit
	else
		puts'wrong input'
	end
end