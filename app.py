import io
import g4f
import time
import json
import requests
from flask import Flask, request


BOT_TOKEN = '5776926867:AAG-IBvvIkACVRMP85Kq2HauYVNEjbehqLk'
ADMIN = 5934725286
GROUP = -4099666754

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_webhook():
    try:
        process(json.loads(request.get_data()))
        return 'Success!'
    except Exception as e:
        print(e)
        return 'Error'

def process(update):
    if 'message' in update:
        if 'text' in update['message']:
            message = update['message']['text']
            if message == '/start':
                if not any(str(update['message']['from']['id']) in line.split()[0] for line in open('users.txt')):
                    with open('users.txt', 'a') as file:
                        file.write(f"{update['message']['from']['id']} {update['message']['from']['first_name'].split()[0]}\n")
                    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',params={'chat_id': update['message']['from']['id'],'text': f"✅ Hello <a href='tg://user?id={update['message']['from']['id']}'>{update['message']['from']['first_name']}</a> !", 'parse_mode': 'HTML'})
                with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                    file.write(' ')
                menu(update['message']['from']['id'], '_Welcome!_')
            elif message == 'Task 1':
                with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                    file.write(' ')
                data = {
                    'chat_id': update['message']['from']['id'],
                    'text': f"_Currently we are working to add this function_",
                    'parse_mode': 'Markdown'
                }
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
            elif message == 'Task 2':
                with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                    file.write('2 N')
                data = {
                    'chat_id': update['message']['from']['id'],
                    'text': f"_Now send your essay topic_",
                    'parse_mode': 'Markdown'
                }
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
            elif message == '/menu':
                menu(update['message']['from']['id'], '_Choose!_')
            elif message == '/INITIALIZE' and update['message']['from']['id'] == ADMIN:
                initialize()
            elif message == '/USERS' and update['message']['from']['id'] == ADMIN:
                send_users()
            else:
                try:
                    with open(f"{update['message']['from']['id']}.txt", 'r') as file:
                        model = file.readline()
                    if model == ' ':
                        menu(update['message']['from']['id'], '_Choose!_')
                    elif len(model) == 1 or len(model) == 3:
                        send_topic(update['message']['from']['id'], update['message']['text'])
                    else:
                        initial(update['message']['from']['id'], update['message']['text'], model[0], model[2:])
                except:
                    data = {
                        'chat_id': update['message']['from']['id'],
                        'text': f"_System has been updated! please re /start_",
                        'parse_mode': 'Markdown'
                    }
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
def send_users():
    with open('users.txt', 'r') as file:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",params={'chat_id': ADMIN},files={'document': ('Users.txt', io.StringIO(''.join(file.readlines())))})
    file.close()
    return

def send_topic(user_id, topic):
    with open(f"{user_id}.txt", 'r') as file:
        mode = file.readline()[0]
    with open(f"{user_id}.txt", 'w') as file:
        file.write(f"{mode} {topic}")
    data = {
        'chat_id': user_id,
        'text': f"_Now send your essay_",
        'parse_mode': 'Markdown'
    }
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
    return

def initial(user_id, query, mode, topic):
    if mode == '1':
        instruction = """You must tell my band score based on the provided below and the topic provided below be very strict and tough while giving higher the band score, if your are unsure about the band score you can give somewhere in the middle (e.g if the essay worth neither 5 nor 6 you can give 5.5). Your response structure must follow to this: bolded band score in first line followed by my original essay with errors highlighted in italic, followed by structured brief and accurate and precise description of errors followed by structured ways to improve for my next essays mentioned in 1,2,3... 
Criteria:
Band 9:
Task achievement
All the requirements of the task are fully and appropriately satisfied.

There may be extremely rare lapses in content.

Coherence and cohesion
The message can be followed effortlessly.

Cohesion is used in such a way that it very rarely attracts attention.

Any lapses in coherence or cohesion are minimal.

Paragraphing is skilfully managed.

Lexical resource
Full flexibility and precise use are evident within the scope of the task.

A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features.

Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.

Grammatical range and accuracy
A wide range of structures within the scope of the task is used with full flexibility and control.

Punctuation and grammar are used appropriately throughout.

Minor errors are extremely rare and have minimal impact on communication. 
Band 8:
Task achievement
The response covers all the requirements of the task appropriately, relevantly and sufficiently.

(Academic) Key features are skilfully selected, and clearly presented, highlighted and illustrated.

(General Training) All bullet points are clearly presented, and appropriately illustrated or extended.

There may be occasional omissions or lapses in content.
Coherence and cohesion
The message can be followed with ease.

Information and ideas are logically sequenced, and cohesion is well managed.

Occasional lapses in coherence or cohesion may occur.

Paragraphing is used sufficiently and appropriately.
Lexical resource
A wide resource is fluently and flexibly used to convey precise meanings within the scope of the task.

There is a skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation.

Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.
Grammatical range and accuracy
A wide range of structures within the scope of the task is flexibly and accurately used.

The majority of sentences are error-free, and punctuation is well managed.

Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication. 
Band 7:
Task achievement
The response covers the requirements of the task.

The content is relevant and accurate – there may be a few omissions or lapses. The format is appropriate.

(Academic) Key features which are selected are covered and clearly highlighted but could be more fully or more appropriately illustrated or extended.

(Academic) It presents a clear overview, the data are appropriately categorised, and main trends or differences are identified.

(General Training) All bullet points are covered and clearly highlighted but could be more fully or more appropriately illustrated or extended. It presents a clear purpose. The tone is consistent and appropriate to the task. Any lapses are minimal.
Coherence and cohesion
Information and ideas are logically organised and there is a clear progression throughout the response. A few lapses may occur.

A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some over/under use.
Lexical resource
The resource is sufficient to allow some flexibility and precision.

There is some ability to use less common and/or idiomatic items.

An awareness of style and collocation is evident, though inappropriacies occur.

There are only a few errors in spelling and/or word formation, and they do not detract from overall clarity.
Grammatical range and accuracy
A variety of complex structures is used with some flexibility and accuracy. 
Band 6:
Task achievement
The response focuses on the requirements of the task and an appropriate format is used.

(Academic) Key features which are selected are covered and adequately highlighted. A relevant overview is attempted. Information is appropriately selected and supported using figures/data.

(General Training) All bullet points are covered and adequately highlighted. The purpose is generally clear. There may be minor inconsistencies in tone.

Some irrelevant, inappropriate or inaccurate information may occur in areas of detail or when illustrating or extending the main points.

Some details may be missing (or excessive) and further extension or illustration may be needed.

Coherence and cohesion
Information and ideas are generally arranged coherently and there is a clear overall progression.

Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission.

The use of reference and substitution may lack flexibility or clarity and result in some repetition or error.

Lexical resource
The resource is generally adequate and appropriate for the task.

The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice.

If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy.

There are some errors in spelling and/or word formation, but these do not impede communication.

Grammatical range and accuracy
A mix of simple and complex sentence forms is used but flexibility is limited.

Examples of more complex structures are not marked by the same level of accuracy as in simple structures.

Errors in grammar and punctuation occur, but rarely impede communication.
Band 5:
Task achievement
The response generally addresses the requirements of the task. The format may be inappropriate in places.

(Academic) Key features which are selected are not adequately covered. The recounting of detail is mainly mechanical. There may be no data to support the description.

(General Training) All bullet points are presented but one or more may not be adequately covered. The purpose may be unclear at times. The tone may be variable and sometimes inappropriate.

There may be a tendency to focus on details (without referring to the bigger picture).

The inclusion of irrelevant, inappropriate or inaccurate material in key areas detracts from the task achievement.

There is limited detail when extending and illustrating the main points

Coherence and cohesion
Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response.

The relationship of ideas can be followed but the sentences are not fluently linked to each other.

There may be limited/overuse of cohesive devices with some inaccuracy.

The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution.

Lexical resource
The resource is limited but minimally adequate for the task.

Simple vocabulary may be used accurately but the range does not permit much variation in expression.

There may be frequent lapses in the appropriacy of word choice, and a lack of flexibility is apparent in frequent simplifications and/or repetitions.

Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.

Grammatical range and accuracy
The range of structures is limited and rather repetitive.

Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences.

Grammatical errors may be frequent and cause some difficulty for the reader.

Punctuation may be faulty.
Band 4:
Task achievement
The response is an attempt to address the task.

(Academic) Few key features have been selected.

(General Training) Not all bullet points are presented.

(General Training) The purpose of the letter is not clearly explained and may be confused.The tone may be inappropriate.

The format may be inappropriate.

Key features/bullet points which are presented may be irrelevant, repetitive, inaccurate or inappropriate.

Coherence and cohesion
Information and ideas are evident but not arranged coherently, and there is no clear progression within the response.

Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive.

There is inaccurate use or a lack of substitution or referencing

Lexical resource
The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively.

There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material).

Inappropriate word choice and/or errors in word formation and/or in spelling may impede meaning

Grammatical range and accuracy
A very limited range of structures is used.

Subordinate clauses are rare and simple sentences predominate.

Some structures are produced accurately but grammatical errors are frequent and may impede meaning.

Punctuation is often faulty or inadequate 
Band 3:
Task achievement
The response does not address the requirements of the task (possibly because of misunderstanding of the data/diagram/situation).

Key features/bullet points which are presented may be largely irrelevant.

Limited information is presented, and this may be used repetitively

Coherence and cohesion
There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other.

Minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship between ideas.

There is difficulty in identifying referencing.

Lexical resource
The resource is inadequate (which may be due to the response being significantly underlength).

Possible over-dependence on input material or memorised language.

Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning.

Grammatical range and accuracy
Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through.

Length may be insufficient to provide evidence of control of sentence forms.
Band 2:
Task achievement
The content barely relates to the task.

Coherence and cohesion
There is little relevant message, or the entire response may be off-topic.

There is little evidence of control of organisational features.

Lexical resource
The resource is extremely limited with few recognisable strings, apart from memorised phrases.

There is no apparent control of word formation and/or spelling.

Grammatical range and accuracy
There is little or no evidence of sentence forms (except in memorised phrases). 
Band 1:
Task achievement
Responses of 20 words or fewer are rated at Band 1.

The content is wholly unrelated to the task.

Any copied rubric must be discounted.

Coherence and cohesion
Responses of 20 words or fewer are rated at Band 1.

The writing fails to communicate any message and appears to be by a virtual non-writer.

Lexical resource
Responses of 20 words or fewer are rated at Band 1.

No resource is apparent, except for a few isolated words.

Grammatical range and accuracy
Responses of 20 words or fewer are rated at Band 1.

No rateable language is evident
Band 0:
Should only be used where a candidate did not attend or attempt the question in any way, used a language other than English throughout, or where there is proof that a candidate’s answer has been totally memorised.

Here is essay topic:
"""
    else:
        instruction = """You must tell my band score based on the provided below and the topic provided below be very strict and tough while giving higher the band score, if your are unsure about the band score you can give somewhere in the middle (e.g if the essay worth neither 5 nor 6 you can give 5.5). Your response structure must follow to this: band score in first line followed by my original essay's errors highlighted in italic and corrected version of my error in parallel, followed by structured brief and accurate and precise description of errors followed by structured ways to improve for my next essays mentioned in 1,2,3...While answering you should avoid: stating the description of any band score. I do not have to cite or use reference in my essay. Note: *This is bold text*, _This is italic text_ So use bold text or italic for highlighting
Band 0
Should only be used where a candidate did not attend or attempt the question in any way, used a language other than English, or where there is proof that a candidate’s answer has been totally memorised.
Band 1
Task response
Responses of 20 words or fewer are rated at Band 1.

The content is wholly unrelated to the prompt.

Any copied rubric must be discounted.

Coherence and cohesion
Responses of 20 words or fewer are rated at Band 1.

The writing fails to communicate any message and appears to be by a virtual non-writer.

Lexical resource
Responses of 20 words or fewer are rated at Band 1.

No resource is apparent, except for a few isolated words.

Grammatical range and accuracy
Responses of 20 words or fewer are rated at Band 1.

No rateable language is evident.
Band 2
Task response
The content is barely related to the prompt.

No position can be identified.

There may be glimpses of one or two ideas without development.

Coherence and cohesion
There is little relevant message, or the entire response may be off-topic.

There is little evidence of control of organisational features.

Lexical resource
The resource is extremely limited with few recognisable strings, apart from memorised phrases.

There is no apparent control of word formation and/or spelling.

Grammatical range and accuracy
There is little or no evidence of sentence forms (except in memorised phrases).
Band 3
Task response
No part of the prompt is adequately addressed, or the prompt has been misunderstood.

No relevant position can be identified, and/or there is little direct response to the question/s.

There are few ideas, and these may be irrelevant or insufficiently developed.

Coherence and cohesion
There is no apparent logical organisation. Ideas are discernible but difficult to relate to each other.

There is minimal use of sequencers or cohesive devices. Those used do not necessarily indicate a logical relationship between ideas.

There is difficulty in identifying referencing.

Any attempts at paragraphing are unhelpful.

Lexical resource
The resource is inadequate (which may be due to the response being significantly underlength). Possible over-dependence on input material or memorised language.

Control of word choice and/or spelling is very limited, and errors predominate. These errors may severely impede meaning

Grammatical range and accuracy
Sentence forms are attempted, but errors in grammar and punctuation predominate (except in memorised phrases or those taken from the input material). This prevents most meaning from coming through.

Length may be insufficient to provide evidence of control of sentence forms.
Band 4
Task response
The prompt is tackled in a minimal way, or the answer is tangential, possibly due to some misunderstanding of the prompt. The format may be inappropriate.

A position is discernible, but the reader has to read carefully to find it.

Main ideas are difficult to identify and such ideas that are identifiable may lack relevance, clarity and/or support.

Large parts of the response may be repetitive.
Coherence and cohesion
Information and ideas are evident but not arranged coherently and there is no clear progression within the response.

Relationships between ideas can be unclear and/or inadequately marked. There is some use of basic cohesive devices, which may be inaccurate or repetitive.

There is inaccurate use or a lack of substitution or referencing.

There may be no paragraphing and/or no clear main topic within paragraphs.
Lexical resource
The resource is limited and inadequate for or unrelated to the task. Vocabulary is basic and may be used repetitively.

There may be inappropriate use of lexical chunks (e.g. memorised phrases, formulaic language and/or language from the input material).

Inappropriate word choice and/or errors in word formation and/or in spelling may impede meaning

Grammatical range and accuracy
A very limited range of structures is used.

Subordinate clauses are rare and simple sentences predominate.Some structures are produced accurately but grammatical errors are frequent and may impede meaning.

Punctuation is often faulty or inadequate. 
Band 5
Task response
The main parts of the prompt are incompletely addressed. The format may be inappropriate in places.

The writer expresses a position, but the development is not always clear.

Some main ideas are put forward, but they are limited and are not sufficiently developed and/or there may be irrelevant detail.

There may be some repetition.

Coherence and cohesion
Organisation is evident but is not wholly logical and there may be a lack of overall progression. Nevertheless, there is a sense of underlying coherence to the response.

The relationship of ideas can be followed but the sentences are not fluently linked to each other.

There may be limited/overuse of cohesive devices with some inaccuracy.

The writing may be repetitive due to inadequate and/or inaccurate use of reference and substitution.

Paragraphing may be inadequate or missing.

Lexical resource
The resource is limited but minimally adequate for the task.

Simple vocabulary may be used accurately but the range does not permit much variation in expression.

There may be frequent lapses in the appropriacy of word choice and a lack of flexibility is apparent in frequent simplifications and/or repetitions.

Errors in spelling and/or word formation may be noticeable and may cause some difficulty for the reader.

Grammatical range and accuracy
The range of structures is limited and rather repetitive.

Although complex sentences are attempted, they tend to be faulty, and the greatest accuracy is achieved on simple sentences.

Grammatical errors may be frequent and cause some difficulty for the reader.

Punctuation may be faulty.

Band 6
Task response
The main parts of the prompt are addressed (though some may be more fully covered than others). An appropriate format is used.

A position is presented that is directly relevant to the prompt, although the conclusions drawn may be unclear, unjustified or repetitive.

Main ideas are relevant, but some may be insufficiently developed or may lack clarity, while some supporting arguments and evidence may be less relevant or inadequate.

Coherence and cohesion
Information and ideas are generally arranged coherently and there is a clear overall progression.Cohesive devices are used to some good effect but cohesion within and/or between sentences may be faulty or mechanical due to misuse, overuse or omission.

The use of reference and substitution may lack flexibility or clarity and result in some repetition or error.

Paragraphing may not always be logical and/or the central topic may not always be clear.

Lexical resource
The resource is generally adequate and appropriate for the task.

The meaning is generally clear in spite of a rather restricted range or a lack of precision in word choice.

If the writer is a risk-taker, there will be a wider range of vocabulary used but higher degrees of inaccuracy or inappropriacy.

There are some errors in spelling and/or word formation, but these do not impede communication.

Grammatical range and accuracy
A mix of simple and complex sentence forms is used but flexibility is limited.

Examples of more complex structures are not marked by the same level of accuracy as in simple structures.

Errors in grammar and punctuation occur, but rarely impede communication

Band 7
Task response
The main parts of the prompt are appropriately addressed.

A clear and developed position is presented.

Main ideas are extended and supported but there may be a tendency to over-generalise or there may be a lack of focus and precision in supporting ideas/material.

Coherence and cohesion
Information and ideas are logically organised, and there is a clear progression throughout the response. (A few lapses may occur, but these are minor.)

A range of cohesive devices including reference and substitution is used flexibly but with some inaccuracies or some over/under use.

Paragraphing is generally used effectively to support overall coherence, and the sequencing of ideas within a paragraph is generally logical.

Lexical resource
The resource is sufficient to allow some flexibility and precision.

There is some ability to use less common and/or idiomatic items.

An awareness of style and collocation is evident, though inappropriacies occur.

There are only a few errors in spelling and/or word formation and they do not detract from overall clarity.

Grammatical range and accuracy
A variety of complex structures is used with some flexibility and accuracy.

Grammar and punctuation are generally well controlled, and error-free sentences are frequent.

Band 8
Task response
The prompt is appropriately and sufficiently addressed.

A clear and well-developed position is presented in response to the question/s.

Ideas are relevant, well extended and supported.

There may be occasional omissions or lapses in content.
Coherence and cohesion
The message can be followed with ease.

Information and ideas are logically sequenced, and cohesion is well managed.

Occasional lapses in coherence and cohesion may occur.

Paragraphing is used sufficiently and appropriately.
Lexical resource
A wide resource is fluently and flexibly used to convey precise meanings.

There is skilful use of uncommon and/or idiomatic items when appropriate, despite occasional inaccuracies in word choice and collocation.

Occasional errors in spelling and/or word formation may occur, but have minimal impact on communication.
Grammatical range and accuracy
A wide range of structures is flexibly and accurately used.

The majority of sentences are error-free, and punctuation is well managed.

Occasional, non-systematic errors and inappropriacies occur, but have minimal impact on communication
Band 9
Task response
The prompt is appropriately addressed and explored in depth.

A clear and fully developed position is presented which directly answers the question/s.

Ideas are relevant, fully extended and well supported.

Any lapses in content or support are extremely rare
Coherence and cohesion
The message can be followed effortlessly.

Cohesion is used in such a way that it very rarely attracts attention.

Any lapses in coherence or cohesion are minimal.

Paragraphing is skilfully managed

Lexical resource
Full flexibility and precise use are widely evident.

A wide range of vocabulary is used accurately and appropriately with very natural and sophisticated control of lexical features.

Minor errors in spelling and word formation are extremely rare and have minimal impact on communication.
Grammatical range and accuracy
A wide range of structures is used with full flexibility and control.

Punctuation and grammar are used appropriately throughout.

Minor errors are extremely rare and have minimal impact on communication."""
    
    auth = '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'
    provider = g4f.Provider.DeepInfra
    model = "meta-llama/Llama-2-70b-chat-hf"
    response = g4f.ChatCompletion.create(
        model=model,
        provider=provider,
        messages=[{'role': 'user', 'content': instruction + topic + "\n\nHere is my essay itself\n\n" + query}],
        stream=True,
        # meta-llama/Llama-2-70b-chat-hf - good feedback
        # meta-llama/Llama-2-7b-chat-hf - quite strict
    )
    output = ""
    edit_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': user_id, 'text': f'✅ _Your Task {mode} is being checked..._','parse_mode': 'Markdown'}).json()['result']['message_id']
    start = time.time()
    for message in response:
        output += message
        if time.time() - start > 2:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText', json={'chat_id': user_id,'text': f'{output}', 'message_id': edit_id, 'parse_mode': 'Markdown'}).json()
            start += 2
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': user_id, 'text': output, 'message_id': edit_id, 'parse_mode': 'Markdown'})
    with open(f"{user_id}.txt", 'w') as file:
        file.write(' ')
    return

def menu(user_id, text):
    keyboard = {
        'keyboard': [
            ['Task 1','Task 2']
        ],
        'one_time_keyboard': False,
        'resize_keyboard': True
    }
    data = {
        'chat_id': user_id,
        'text': text,
        'reply_markup': json.dumps(keyboard),
        'parse_mode' : 'Markdown'
    }
    print(requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data).json())
    return

def initialize():
    with open('users.txt', 'r') as file:
        for line in file.readlines():
            with open(f'{line.split()[0]}.txt', 'w') as f:
                f.write(' ')
    return


if __name__ == '__main__':
    app.run(debug=False)
