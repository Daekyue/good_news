
text = """
"As does any major competitive film festival, the International Documentary Film Festival Amsterdam (IDFA) has its own development sidebar for projects in their early stages. IDFA’s Forum on Wednesday, as the festival hits the midway point, announced winners for the section’s 2024 awards. The honors will help support these films in their journey ahead out of Europe’s premier documentary film festival — and an essential global crossroads for nonfiction films.Ibrahim Omar’s project “Dry Sky” won the IDFA Forum Award for Best Pitch, while Lana Y. Daher’s “Do You Love Me” took home the Forum Award for Best Rough Cut, and the DocLab Forum Award went to “Amorphous” by May Abdalla.Regarding “Do You Love Me,” produced by Lana Y. Daher, the jury — consisting of Burcu Melekoglu and Mandisa Zitha — said: “We are delighted to present the Jury Award for the most outstanding film about to be released to the filmmaking team of ‘Do You Love Me.’ Lana Y. Daher masterfully weaves a delicate and poignant story of a city and its heartbreaking yet resilient history. Through the evocative use of archival materials from Lebanese cinema, she appropriates the visuals of the city from films as a representation of the cyclical history and nature of memories, bringing to life a narrative that is both deeply personal and profoundly universal. The work stands as a testament to the power of memory and art in navigating collective grief and renewal.”Receiving an inaugural award, “Looking for the Mermaid” by Yara Costa won the Producers Connection Award. Each award comes with a cash prize of €1,500. “Do You Love Me,” meanwhile, will also receive closed captioning and subtitles from inVision Subtitling.Elsewhere at the Forum, when prizes were shared at the Felix Meritis culture center in Amsterdam, “Concrete Land” by Asmahan Bkerat and “The Beauty of Errors” by Jukka Kärkkäinen were recognized with special mentions for the IDFA Forum Award. “The Four Floors of Faneuil Hall” by Simon Wood and Meghna Singh was recognized with an honorable mention for the DocLab Forum Award.“For an articulation of a subtle cinematic language and a courageous proposal of healing. Told through a unique and critical inside perspective we look forward to a collective endeavor to imagine new futures. It takes a village,” said jury members Dorota Lech and Malin Huber of “Dry Sky.”“The world is disappearing before our eyes. That is a strong statement in itself. But the winning project also brings forth the idea that cinema can help preserve dying worlds while at the same time enriching our imagination with new possibilities of being together and of making films. The presentation we witnessed here at Producers Connection has inspired us to award the Producers Connection Award for most creative project with exciting collaborative potential to ‘Looking for the Mermaid by Yara Costa. We hope this incentive will spark interest for the creative collaborations the filmmaker is looking for,” said jurors Bianca Oana and Daan Vermeulen about “Looking for the Mermaid.”The IDFA DocLab Forum jury, consisting of Jazia Hammoudi and Liz Rosenthal, said about “Amorphous” by May Abdalla: “’Amorphous’ is this year’s winner because of its ingenious use of play for a transformational purpose in relation to the crisis in self-image and body dysmorphia. Its messaging is experiential rather than didactic, making it appropriate for all kinds of audiences and demographics. Its design and format present a viable path forward for the immersive field and will appeal to diverse immersive media spaces.”Of “The Four Floors of Faneuil Hall,” the jury members said: “The use of space and architecture to ground their story imbues the project with narrative clarity that makes their point crystal clear about the contradiction of democratic society built on legacies of slavery, genocide and colonialism. The project’s installation format makes it adaptable to many contexts, which opens up the possibility of future iterations beyond Faneuil Hall itself.”IDFA runs through Sunday, November 24 in Amsterdam."
"""


from transformers import pipeline
import pandas as pd
import json



# BERT NER 파이프라인 로드
nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")


def keywords_extract(text):

    # NER 실행
    entities = nlp(text)

    # 스코어 기준으로 정렬
    sorted_entities = sorted(entities, key=lambda x: x['score'], reverse=True)

    ent = pd.DataFrame(sorted_entities)

    # 공백이 있는 단어만 추출
    ent_df = ent[ent['word'].str.contains(' ')]

    # 따옴표 제거
    ent_df['word'] = ent_df['word'].str.replace(r"‘ |“ | ”| ’ | ‘| “|” |’ ", "", regex=True)

    # 중복 제거
    ent_df = ent_df.drop_duplicates(subset=['word'])

    return ent_df.iloc[0:5,]['word']



def process_and_translate_json(input_file, output_file):
    # JSON 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for d in data:

        content = d["Content"]
        
        keywords = keywords_extract(content)
        
        d['Keywords'] = ', '.join(list(keywords))
    
    # 번역된 데이터를 다시 JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



process_and_translate_json("articles.json", "test.json")