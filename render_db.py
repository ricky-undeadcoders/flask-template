#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sys import argv
from datetime import datetime, timedelta

from application.models import *

if len(argv) > 1:
    if argv[1].lower() == 'production':
        from application.config.production_config import SQLALCHEMY_DATABASE_URI
    if argv[1].lower() == 'qa':
        from application.config.qa_config import SQLALCHEMY_DATABASE_URI
else:
    from application.config.test_config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def populate_roles():
    sample_roles = [{'name': 'blogger', 'description': 'Ability to post new blogs and edit them'},
                    {'name': 'commenter', 'description': 'Ability to post new comments and edit them'},
                    {'name': 'admin', 'description': 'Ability to log in as admin'}]

    for role in sample_roles:
        this_role = Role(**role)
        session.add(this_role)
        session.commit()


def populate_admin_roles():
    sample_roles = [{'name': 'superuser', 'description': 'SuperUser permissions'}]

    for role in sample_roles:
        this_role = Role(**role)
        this_role.is_admin = True
        session.add(this_role)
        session.commit()


def populate_base_users():
    commenter_role = session.query(Role).filter(Role.name == 'commenter').first()
    blogger_role = session.query(Role).filter(Role.name == 'blogger').first()
    admin_role = session.query(Role).filter(Role.name == 'admin').first()
    sample_users = [{'username': 'ricky',
                     'first_name': 'Ricky',
                     'last_name': 'Whitaker',
                     'password': 'abc123',
                     'email': 'ricky.whitaker@undeadcodersociety.com',
                     'confirmed_at': datetime.utcnow(),
                     'bio': 'I am the founder of Undead Coder Society and co-founder of several other ventures that are currently in the making.  I took a leave from my job in March 2016, travelled for a while, and then came back and starting coding again.<br><br>Currently I am building web applications using Python; and I will post about my mis-adventures with Flask, Redis, Celery, Docker, Kubernetes, SQL, Mongo and others.... and about my time off from work and working without getting paid.'},
                    {'username': 'asa',
                     'password': 'ames',
                     'first_name': 'Asa',
                     'last_name': 'Ames',
                     'email': 'asa.ames@undeadcodersociety.com',
                     'confirmed_at': datetime.utcnow(),
                     'bio': "My name is Asa Ames. I'm currently in charge of all things front-end at UCS. Everything from the front-end architecture, to the templating structure, styling, scripting, front-end package integration, and even the UI design is my domain. I'm always learning and trying to progress my career as a frontend guru. I love programming, playing music, and generally having a great time, all the time."},
                    # {'username': 'priscilla',
                    #  'password': 'jupe',
                    #  'first_name': 'Priscilla',
                    #  'last_name': 'Jupe',
                    #  'email': 'priscilla.jupe@undeadcodersociety.com',
                    #  'confirmed_at': datetime.utcnow(),
                    #  'bio': "My name is Asa Ames. I'm currently in charge of all things front-end at UCS. Everything from the front-end architecture, to the templating structure, styling, scripting, front-end package integration, and even the UI design is my domain. I'm always learning and trying to progress my career as a frontend guru. I love programming, playing music, and generally having a great time, all the time."}
                    ]

    for sample_user in sample_users:
        bio = Bio(**{'text': sample_user.pop('bio')})
        user = User(**sample_user)
        user.bio = bio
        user.roles = [commenter_role, blogger_role, admin_role]
        session.add(user)
        session.commit()


def populate_posts():
    asa = session.query(User).filter_by(username='asa').first()
    ricky = session.query(User).filter_by(username='ricky').first()
    sample_posts = [{'title': 'My First Flask Application',
                     'user': ricky,
                     'active': True,
                     'create_date': datetime.now() + timedelta(days=-5, hours=5, minutes=5),
                     'body': '''
I wrote my first Flask application over a long weekend in 2016. I'd never programmed an application from top to bottom before, and starting from scratch was like drinking information from a firehose. 
<br/><br/>
My end goal was to put an application on the web that would utilize Ebay's API to look at the sales potential of item lists that were provided to me via Excel docs or a webpage. I would gather data from either a CSV import or by screen scraping it from a site my friend managed, and then feed it to Ebay's Finder API to gather item lists for interpretation about how often an item sold, when it had last sold, etc. Now, a great way to have handled this project would have been to map out exactly what I intended to build, including the pages that I was going to include on my site, the packages I was going to use for the screen-scraping, what my application was going to look like. But the truth is that planning has never been my strong suit, so I dove in head first and stated coding.
<br/><br/>
It took me a couple of days to finish the initial project, one giant file full of templates, filters, helpers, views, one screen scraper, one CSV import module, a bunch of terrible looking HTML and some particularly mediocre javascript. But it existed, and it (mostly) worked! 
<br/><br/>
So I went to meet with the friend that I'd built it for. I was super proud of the work I'd done, about how quickly I'd learned something new and how well the app worked, and he kind of shrugged and started pointing out the things it didn't do. So I learned something about user expectations in the 21st century, and exactly what it would take to build a successful app.
<br/><br/>
Next time I'll post about how I took the next big step with that little app and got it on the internet.
'''
                     },
                    {'title': 'Getting My First Application Online',
                     'user': ricky,
                     'active': True,
                     'body': '''
The internet has always been a bit of a black box to me. I had an idea about what it was... a bunch of servers communicating with each other, but in the end that's about all I understood about it. Even after five years of working in the tech industry in various capacities I still didn't have a clear picture of it. Sure, I knew buzz words and pieces of it, but if you asked me how you stood up a website and hosted it from scratch, I would have been at a loss. So, it became one of my goals to do just that: stand up a website from scratch.
<br/><br/>
One of the things I found while working 40 hours at a job was that I routinely had no energy to dedicate to my own personal growth. 40 hours would turn into 50 or 60 hours, and by the time I was done all I wanted to do was have a drink and relax. Video games and television became my relax time, and so my website building goal remained far off. Even though I could modify a .NET stack, or add a page to an existing site, or modify content of a site, I still never stood one up on my own.
<br/><br/>
After I built my first Flask application, getting it online was the next big project. But unlike Flask, which is so conveniently built with Python, standing up a website required something I had embarrassingly little of; server knowledge. Luckily I had a mentor who had some experience in that topic who was willing to work through that with me; and so we met at a coffee shop for a few hours one weekend afternoon.
<br/><br/>
That workday was mostly me watching while my mentor worked through creating a Docker container based off of my code that would run. He troubleshot through issues that would take me a solid year afterwards to understand, but after a few hours of digging through the weeds on his part, and semi-comprehension on my part, we had it; my site was online!
<br/><br/>
My reaction was immediate; excitement to the point of euphoria. I think I actually kind of freaked my teacher out because of how excited I got. Regardless of whether I fully understood the process, or the fact that I hadn't even been doing the Dockering, my objective had been realized in a very non-trivial way. I had a site that was online from scratch (more or less). Of course I wasn't hosting servers or splitting into the city power-grid Guilfoyle style, but I didn't really want any of that. One of the primary lessons I have learned over the years is that there are shoulders of giants to build off of; and it's silly not to start there.
<br/><br/>
So there it started; I spent the next year learning the key components myself, but that's a blog entry for another day.
                     '''},
                    {'title': 'My Journey Into Frontend',
                     'user': asa,
                     'active': True,
                     'create_date': datetime.now() + timedelta(days=-2, hours=-3, minutes=20),
                     'body': '''
My 18-year old self never could have imagined that I would be where I am now in my career. Especially since my 18-year-old self never even had plans of becoming a professional programmer. In those days, I was a fresh-faced college student in my first year of film school, with big plans to become the next Quentin Tarantino.
<br/><br/>
I think it's pretty obvious I did not become the next Quentin Tarantino. And that's more than okay. After graduating with my film degree from UT, the bright and shiny dream of becoming a great filmmaker had all but been replaced by the harsh reality of the intense grind that takes place behind the scenes. Not to mention, financial prospects are generally low for a recent grad trying to make it in the film industry. I have immense respect for my UT friends who are taking on that challenge and in most cases having great success.
<br/><br/>
Near the end of college, another interest of mine was rapidly gaining momentum: Programming. I had taken a Java course in high school and a Python course in college, but in both cases they were just electives and I did not take them very seriously. During my final year of college, I started taking youtube tutorials on HTML, CSS, Javascript... all the Front-end development basics. I was immediately drawn to the creative nature of web development. The endless possibilities of what I could create excited me. After learning the basics, even the most far-flung ideas seemed within reach.
<br/><br/>
Following this, for lack of a better word, epiphany, I devoted myself to making it in the tech industry. Luck had it that I was already living in one of the greatest American tech hubs, Austin, Texas... I was not credentialled or trained to become a software developer, but I proceeded to jump into the industry as a customer support rep and then a product manager. Customer support was not my forte. While I managed to do well in the role, I found it to be utterly exhausting and not even remotely rewarding. Product management was more in line with my creative side as it allowed me to contribute to the design and direction of an enterprise software product.
<br/><br/>
What I really wanted was to become a developer. There are many creative roles involved in software, but in my mind, programmers are the true creators. They are the ones creating and assembling the building blocks on which everything else depends. During those first two years after graduating, I spent most of my free time online learning about web development, as well as game development via Unity3D and C#, hoping to transition into a software developer role at some point. My "big break" came at the very end of 2014, when I was selected to participate in a paid developer training program at an Austin-based software company. After the training program I was immediately hired on as a full-stack developer.
<br/><br/>
Starting off in a full-stack role for my first job as a web developer had its challenges but ultimately ended up being a great way of learning concepts across all webdev disciplines, comprehending how the different areas interact with each other, and discovering my strengths and weaknesses. Slowly but surely, over the past three years, I have managed to narrow down my expertise to the discipline that excites me most: Front-end!
<br/><br/>
Moving forward, I hope to share my discoveries and experiences via this blog as I improve my skills as a front-end developer. Stay tuned for more to come...
'''
                     },
                    {'title': 'The Undead Stack - Frontend Edition',
                     'user': asa,
                     'active': True,
                     'create_date': datetime.now() + timedelta(days=-1, hours=6, minutes=14),
                     'body': '''
As the lead frontend engineer for UCS, it has been my duty to develop a frontend architecture that works best for the size of our applications in terms of efficiency and reusability and also integrates seamlessly with the backend architecture that was built out by my associate, Ricky. That backend architecture is primarily comprised of Flask and MongoDB (though we recently switched over to mySQL for larger applications). I'm sure Ricky will share more about our DevOps workflow and our backend stack in good time. In the meantime, I'll fill you in on the frontend stack and how it evolved to its current state.
<br/><br/>
When we first started building web applications together, I had no idea what direction I would take the frontend. In the beginning, I spent a ton of time exploring various frontend libraries, frameworks, and other tools (compilers, preprocessors, bundlers, etc). I knew I was going to utilize Jinja2 and Bootstrap to start out simply because I was already familiar with using them to build out user interfaces. We've come a long way since then, augmenting our stack with numerous packages and engineering a logical and highly efficient templating structure.
<br/><br/>
But I've also had to cut a few technologies along the way. One major lesson I've learned in my last year is that there is no such thing as a one-size-fits-all frontend architecture. I spent many hours pouring over React and Redux with the intention of integrating it into our stack. Ultimately, I decided to let them go simply because the benefits they provided were not worth the extra time and effort of implementing them our relatively small web applications. I can clearly see how beneficial that tech would be in a large-team setting and on an enterprise application. But since it is just the two of us, I made a conscious effort to keep our stack as lightweight as possible. More recently, I spent some time spinning up a flask app using our base architecture and integrating React into our workflow in order to experiment with single-page application design concepts. It makes for a really interesting symbiotic relationship between Jinja2 templating and React interface-building. But it also adds some unnecessary levels of complexity when you're trying to keep a codebase as accessible as possible.
<br/><br/>
We utilize a wide variety of frontend packages and technologies for various use-cases. Here is a list of the standard frontend tech we use on every application to some extent:
<br/><br/>
<ul>
    <li>HTML5</li>
    <li>CSS3</li>
    <li>SCSS</li>
    <li>JavaScript</li>
    <li>jQuery</li>
    <li>Bootstrap</li>
    <li>AJAX</li>
    <li>jQuery Validate</li>
    <li>Jinja2</li>
</ul>
<br/><br/>
I've also incorporated a number of 3rd-party libraries, plugins, and APIs into our software to assist with some common functionality that is found all over the web. Here are three (with their associated functionality) that I plan to write about my experience with:
<br/><br/>
<ul>
    <li>Online Storefront: <a href='https://getmdl.io/'>Material Design Lite</a></li>
    <li>Calendar: <a href='https://fullcalendar.io/'>FullCalendar</a></li>
    <li>Text Editor: <a href='https://quilljs.com/'>Quill</a></li>
</ul>
<br/><br/>
I'm always learning and trying to stay ahead of the curve in the world of frontend. There is so much awesome stuff that I'm researching all the time and it goes way beyond our current stack. I plan to blog about my takeaways from experimenting with different stacks and libraries, alternate approaches to project structure and workflow, and interesting conceptual topics like PWAs (Progressive Web Applications) and User Interface design. So stay tuned for more!
                    '''
                     }
                    ]

    for post in sample_posts:
        this_post = Post(**post)
        this_post.active = True
        session.add(this_post)
        session.commit()


def populate_content():
    from render_content_text import content_list

    for content in content_list:
        this_content = Content(**content)
        this_content_draft = ContentDraft(**content)
        session.add(this_content)
        session.add(this_content_draft)
        session.commit()


def populate_invitation_emails():
    emails = ['rickster85@aol.com', 'karmabase13@gmail.com', 'priscilla.jupe@undeadcodersociety.com',
              'peej128@gmail.com']

    for email in emails:
        invite = InvitationEmail(email=email)
        session.add(invite)


def populate_faq():
    sample_faq = [{'order': 1,
                   'question': 'How do I send another confirmation email?',
                   'answer': 'Head <a href="/resend-confirmation-email/">here</a>'},
                  ]

    for faq in sample_faq:
        faq_obj = FAQ(**faq)
        session.add(faq_obj)
        session.commit()


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    populate_roles()
    populate_admin_roles()
    populate_base_users()
    populate_content()
    populate_posts()
    populate_invitation_emails()
    populate_faq()


def update_prod_changes():
    pass


if __name__ == "__main__":
    init_db()
