import os
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")
client = OpenAI(api_key=API_KEY)

# Create a folder for meeting transcripts if it doesn't exist
TRANSCRIPTS_DIR = "meeting_transcripts"
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

# The survey text (as provided)
SURVEY_TEXT = """
Attitudes and competencies survey
Rate to which extend each of the statements describes your behavior using the
following scale
1 – I do it very rarely or never
2 – I sometimes do it
3 – I often do that
4 – I always do that
1 In my free time, I enjoy trying things I have not done before.
2 I actively seek help from my colleagues and subordinates in various situations at
work.
3 I use every encounter with a new person to learn something new.
4 I invest time, energy and money in obtaining new knowledge and skills.
5 From time to time, I question my mental models which describe the world.
6 I accept that the expected result may not be achieved the first time.
7 I forward interesting professional articles to my colleagues.
8 I seek new ways to solve existing problems.
9 If colleagues ask me to give them my time, I always try to allocate it in my
schedule.
10 If I have a promising idea, I discuss it with colleagues.
11 I feel comfortable working in a team with members who are stronger and more
competent than me.
12 I share my knowledge, skills, materials and data, even when the recognition of my
input is not guaranteed.
13 I encourage diversity of opinions and approaches among my employees.
14 I recommend interesting films, books and plays to members of my network.
15 I welcome constructive criticism.
16 I am aware that I always have something to learn in the course of my professional
life.
17 I know that the knowledge I possess is not sufficient to solve complex problems.
18 I share knowledge in various ways: I deliver lectures, write articles, organize
seminars, forward interesting ideas, and share them at lunch.
19 I ask for help and feedback without fearing to look incompetent.
20 I can easily say to my colleagues, “I don’t know enough about this”.
21 I inform my colleagues about what is happening in my area of responsibility on a
regular basis.
22 I welcome new experiences in my life.
23 I enjoy working with people whose approaches and methods are different to mine.
24 I easily interact with people whose views in life are different to mine.
25 I enjoy trying new culinary dishes.
26 When I listen, I completely focus on the speaker.
27 During a conversation, I always ask clarifying questions.
28 During a conversation, I listen for most of the time.
29 I use the language that is clear to my conversation partner.
30 When I listen, I support the speaker with remarks and gestures.
31 I easily get along with people who are not members of my team.
32 I use various arguments to convey my point of view, taking into account the
situation and my audience.
33 I don't accept anything at face value, even when it comes from people close to me.
34 I am comfortable to work with people who have different to me temperaments or
outlooks on life.
35 I always find out how my conversation partner understood my words.
36 I constantly raise expectations in interaction with colleagues
37 I initiate discussion of challenges as they arise, without delay.
38 At the end of each important conversation, I summarize what I heard in my own
words and ask for confirmation.
39 Even if I don’t agree with the point of view of another person, I try to listen and
understand their position.
40 During a conversation, I focus on understanding the speaker’s arguments, not on
how to answer them.
41 I help my colleagues to get their work done, even if they have not asked me about
it.
42 I support my colleagues when they decide to take on ambitious tasks.
43 I constantly try new technologies and practices in my work.
44 I share resources and ideas with my colleagues.
45 I systematically compare achieved results with initial plans.
46 I allocate time and resources, including financial funding, to experiment with new
ideas and test hypotheses.
47 I regularly discuss with my colleagues what works and what doesn’t.
48 I publicly admit my mistakes and share the lessons learned with colleagues.
49 I regularly seek feedback.
50 I know exactly what I master at work.
51 I regularly find time and space to reflect on my work and the work of my
colleagues.
52 I know that there are a lot of people around me who I can learn from.
53 I encourage colleagues to try new technologies and practices in their work.
54 During the discussions, I can change my point of view if other participants offer a
convincing facts-based one.
55 I do not criticize an idea straight away; I tend to think about it first.
56 I encourage colleagues to share their opinions and give them freedom to choose
solutions.
57 It is important for me to hear the point of view of my conversation partner before
voicing my own.
58 I use every opportunity to gain new experience.
59 During a conversation, I never get distracted by the phone, computer, etc.
60 Even if I feel that I know what the speaker is talking about, I still listen to them
carefully.
61 I convey the information to my conversation partners with tact and respect.
62 If I have doubts, remarks or questions during the discussion, I voice them.
63 I never criticize people, only the specific ideas that they express.
64 I always analyze the assumptions that the conclusions are drawn on.
65 I regularly reflect on the outcomes of my own actions.
66 I regularly provide constructive feedback and recommendations to my colleagues.
67 I seek new solutions to familiar problems.
68 I formulate hypotheses about new challenges which I face and test them.
69 I constantly ask myself - "Is there another way of doing it?”
70 When I make a mistake, I take it as an opportunity to improve the processes and
find other ways to overcome a challenge.
"""

# The initial meeting transcript (the starting point of the meeting thread)
INITIAL_TRANSCRIPT = """Meeting Transcript
Date: December 5, 2024
Time: 1:00 PM – 2:00 PM (EST)
Meeting Topic: Sprint Review & Planning
________________________________________
1:00 PM – 1:05 PM: Meeting Kickoff
Alex (Project Manager):
"Hello, everyone. Thanks for joining today’s sprint review and planning session. It’s exactly 1:00 PM, so let’s get started. We have a full agenda: we’ll review our last sprint, plan upcoming tasks, and discuss any challenges. I’d like everyone to keep an open mind and a respectful tone."
Sam (Senior Developer):
"Sure, but let’s keep this tight. I have a hard stop at 2:00."
Lisa (Mid-Level Developer):
"Sounds good. I’m ready with my updates whenever we get to them."
Kim (Junior Developer):
"Um, hi. I’m here too. Ready to go."
Mark (UX Designer):
"Awesome. I have some new design ideas for the onboarding flow—I’m excited to share them."
Rahul (QA Engineer):
"Great, let’s dive in. I have some test findings from the last sprint to discuss as well."
________________________________________
1:05 PM – 1:20 PM: Previous Sprint Review
Alex:
"Let’s begin with a quick round-robin on what got completed. Lisa, you first?"
Lisa:
"Sure. I wrapped up the front-end integration for Feature B. The main functionality is working, but there’s a minor UI bug I’m waiting for Mark’s sign-off on—"
Sam (interrupting):
"Oh, come on. You’re not still stuck on that drop-down menu thing, are you? We never even agreed that was necessary."
Lisa:
"Actually, Sam, we did agree on it during our last sprint planning session. I have the design specs—"
Sam:
"Lisa, I’m 99% sure you’re mixing up specs from a different project. We never needed a fancy drop-down for this feature. Let’s not complicate things."
(There’s an awkward silence.)
Alex:
"Let’s not get stuck. Mark, could you confirm if a drop-down was part of your design doc?"
Mark:
"Yes, it was explicitly requested. The user feedback indicated we needed an easy selection mechanism. A drop-down was the simplest route."
Sam:
"Whatever. We’ll check it later. Let’s keep moving."
Rahul:
"From the QA side, I’ve completed about 90% of the test cases for Feature A. There are a few edge cases left, but so far the integration looks solid."
Kim:
"I—uh—I’ve been updating the internal documentation. I’m still working on it, but I should be done by tomorrow."
Alex:
"Okay, thanks, Kim. It’s important we have updated docs. Let’s move to the upcoming features."
________________________________________
1:20 PM – 1:35 PM: Upcoming Features & Priorities
Alex:
"We have a couple of new features proposed for the next sprint. Mark, you wanted to talk about improving the onboarding experience?"
Mark:
"Right, so based on user feedback, new users are struggling to understand the product on first launch. A simple tutorial or guided tour could significantly reduce confusion and drop-off rates."
Sam (raising his voice):
"We don’t have time to pamper users. They can figure it out on their own. If we keep adding fluff, we’ll never finish the core features."
Rahul:
"Sam, in QA we’re seeing the same user confusion. Maybe a small tutorial wouldn’t be that big of a lift. We should at least estimate the work."
Sam:
"Look, I’ve been doing this long enough to know a ‘small’ tutorial is never small. We need to focus on the real development tasks."
Lisa:
"What if we create a scaled-down version first? Just a simple step-by-step to guide users through the basics?"
Sam:
"You’re overthinking it. Let’s not complicate our sprint backlog."
Alex:
"Let’s put the onboarding tutorial on the list as a potential item. We’ll do a quick story-point estimate to see if it’s feasible."
Mark:
"Thank you, Alex. I really think it’s worth the effort."
________________________________________
1:35 PM – 1:45 PM: Roadblocks & Challenges
Alex:
"Next, let’s talk about any roadblocks. Lisa?"
Lisa:
"I’m finding that the code review process is taking too long. We only have one senior dev—Sam—doing reviews, and it’s creating a bottleneck. I’d like us to consider a rotating review schedule."
Sam (dismissive tone):
"We’ve always done code reviews this way. I don’t see why we need to change a system that works."
Lisa:
"But the backlog of PRs is growing. It’s causing delays for the rest of the team."
Rahul:
"Lisa has a point. The QA team can’t test effectively until the changes are merged. Maybe a second reviewer or a buddy system would help?"
Sam:
"Then we get inconsistent quality. I’d rather handle it myself so I know the code meets standards."
Mark:
"I see how it’s important to maintain quality, but maybe we can compromise? Sam, you can focus on more complex PRs, and we delegate simpler ones to others with your guidance."
Sam:
"Fine. I’ll think about it, but no promises."
________________________________________
1:45 PM – 1:55 PM: Next Steps & Assignments
Alex:
"Okay, let’s outline our action items. Lisa and Mark, could you set up a separate meeting to finalize the drop-down UI and discuss the tutorial concept?"
Lisa:
"Sure, Mark and I can do that tomorrow afternoon."
Mark:
"Perfect. I’ll send out a calendar invite."
Alex:
"Sam, could you review Lisa’s latest front-end updates by Thursday?"
Sam:
"Yeah, yeah. I’ll get to it."
Alex:
"Rahul, please complete the remaining edge-case tests and share the results at the next stand-up. Kim, keep working on the internal documentation. I’d like a draft before the mid-sprint check-in next Wednesday."
Kim:
"Got it. I’ll have it finished by then."
Rahul:
"Will do, Alex."
________________________________________
1:55 PM – 2:00 PM: Wrap-Up & Meeting Close
Alex:
"That covers everything on our agenda. Let’s stay on top of these tasks and maintain open communication. Does anyone have anything else before we wrap up?"
Sam:
"Nope. I’m good."
Lisa:
"I think that’s all from my side."
Mark:
"All set, thanks."
Rahul:
"Same here."
Kim:
"I’m good too."
Alex:
"Great. Thanks for your time, everyone. We’ll reconvene next Wednesday for our mid-sprint check-in. Meeting adjourned."
(Sam promptly leaves the call. Mark and Lisa stay on briefly to coordinate meeting times. Kim quietly logs off. Rahul thanks Alex before disconnecting.)
"""

# Initialize the previous transcript with the provided transcript
previous_transcript = INITIAL_TRANSCRIPT

def generate_meeting_transcript(meeting_number, previous_transcript):
    """
    Generates the next meeting transcript given the previous transcript.
    """
    # Construct a detailed prompt that includes all necessary context.
    prompt = f"""
You are to generate the next meeting transcript in a series of synthetic data meetings. Each meeting should continue the thread from the previous one.

Below is a survey of attitudes and competencies on best practices. Participants are evaluated on how well they follow these best practices:
{SURVEY_TEXT}

Meeting participants:
- Alex (Project Manager): Always exemplifies best practices.
- Sam (Senior Developer): Consistently fails to follow best practices (serves as a counter example).
- Lisa (Mid-Level Developer), Kim (Junior Developer), Mark (UX Designer), and Rahul (QA Engineer): Fall in between.

Below is the transcript of the previous meeting:
{previous_transcript}

Using the style, formatting, and tone of the previous transcript, generate the transcript for the next meeting. The new transcript must:
• Begin with a header containing the meeting date, time, and topic.
• Present realistic dialogue and progression of discussion points, reflecting continuity from the previous meeting.
• Showcase Alex’s exemplary behavior and Sam’s counter-example in adherence to best practices.
• Be provided as plain text without any additional commentary.

Meeting transcripts should be around 200 lines total. Make sure meetings are similar in length and complexity to the provided example.

Meeting Transcript:
"""
    # Use the OpenAI ChatCompletion API with GPT-4 (or latest) to generate the transcript
    response = client.chat.completions.create(
        model="o1",
        messages=[
            {"role": "system", "content": "You are a creative assistant that generates realistic meeting transcripts."},
            {"role": "user", "content": prompt}
        ]
    )
    transcript = response.choices[0].message.content
    return transcript

# Generate 24 meeting transcripts sequentially
for meeting_num in tqdm(range(1, 25), desc="Generating Meetings", unit="meeting"):
    transcript = generate_meeting_transcript(meeting_num, previous_transcript)
    
    # Define filename (numbered in the order of meetings)
    filename = os.path.join(TRANSCRIPTS_DIR, f"{meeting_num}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
    
    # Update previous_transcript to the current one for continuity
    previous_transcript = transcript

print("All 24 meeting transcripts have been generated and saved in the 'meeting_transcripts' folder.")
