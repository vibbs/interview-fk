from enum import Enum
from datetime import datetime

class User:

    id =  None
    username = None
    follows = None
    created_on = None

    def __init__(self, id : int,  username:  str) -> None:
       """
        Initialization
       :param id:
       :param username:
       """
       self.id  = id
       self.username = username
       self.follows = []
       self.created_on = datetime.now()


    def follow_user(self, ext_user_id) -> None:
        """
        This function helps adding the user to the following list
        :param ext_user_id:
        :return:
        """
        self.follows.append(ext_user_id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'follows': self.follows,
            'created_on': self.created_on
        }



class Reactions(Enum):

    LAUGH = ''
    CRY = ''
    SMILE = ''
    FROWN = ''
    MEH = ''






class Post:

    id = None
    content = None
    created_by = None
    created_on = None
    reactions = None
    comments = None

    def __init__(self, id, content, created_by):

        self.id = id
        self.content = content
        self.created_by = created_by # This is the user id
        self.created_on = datetime.now()
        self.reactions = {}

        self.comments = []


    def add_reaction(self, reaction_type) -> bool:


        if reaction_type not in Reactions.__members__:
            return False


        if reaction_type not in self.reactions:
            self.reactions[reaction_type] = 1
        else:
            self.reactions[reaction_type] += 1

        return True


    def add_comment(self, comment):

        if not isinstance(comment, Post):
            return False

        self.comments.append(comment)


    def serialize(self):
        return {
            'id': self.id,
            'content' : self.content,
            'created_by' : self.created_by,
            'created_on' : self.created_on,
            'reactions' : self.reactions,
            'comments' : [e.serialize() for e in self.comments],
        }




class Comments(Post):

    commented_on = None


    def __init__(self, id, content, created_by, commented_on):
        self.id = id
        self.content = content
        self.created_by = created_by  # This is the user id
        self.created_on = datetime.now()
        self.reactions = {}
        self.commented_on = commented_on

    def serialize(self):
        return {
            'id': self.id,
            'content' : self.content,
            'created_by' : self.created_by,
            'created_on' : self.created_on,
            'reactions' : self.reactions
        }