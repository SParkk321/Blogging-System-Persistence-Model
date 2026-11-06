from blogging.post import Post
from blogging.dao.post_dao import PostDAO
from blogging.configuration import Configuration
import pickle

# Concrete DAO for Post
class PostDAOPickle(PostDAO):

    def __init__(self, blog):
        self.autosave = Configuration.autosave
        self.blog = blog
        
        if self.autosave:
            self.posts = self.load_posts()

        else:
            self.posts = {}
    

    def get_file_path(self) -> str:

        directory = Configuration.records_path
        extension = Configuration.records_extension
        id = str(self.blog.id)

        file_path = directory + '/' + id + extension
        return file_path 

    
    def load_posts(self):
        file_path = self.get_file_path()
        posts = {}

        try:
            with open(file_path, "rb") as file:
                posts_list = pickle.load(file)
                for current_post in posts_list:
                    posts[current_post.code] = current_post
                
                if len(posts) > 0:
                    self.blog.next_post_code = max(posts.keys()) + 1
                else:
                    self.blog.next_post_code = 1

                return posts

        except FileNotFoundError:
            return {}

    
    def save_posts(self):
        file_path = self.get_file_path()

        if self.autosave:

            with open(file_path, "wb") as file:

                pickle.dump(list(self.posts.values()), file)


    
    def search_post(self, key: int):
        """
        Search and return the requested post with the given post code.
        Returns None if the post does not exists.
        """
        return self.posts.get(key)


    def create_post(self, post: Post):
        """
        Create a new given Post.
        Return the newly created Post.
        """
        self.posts[post.code] = post
        self.save_posts()
        return post


    def retrieve_posts(self, search_string):
        """
        Retrieve post from given search string.
        Returns a list of Posts that references the given search string.
        Returns an empty list if none is found.
        """
        related_posts = []
        if search_string is None:
            return related_posts
            
        search = search_string.upper()
        for current_post in self.posts.values():
            if search in current_post.title.upper() or search in current_post.text.upper():
                related_posts.append(current_post)

        return related_posts


    def update_post(self, key, new_title, new_text):
        """
        Update a post with the given key, title, and test.
        Returns True if update was successful.
        Returns False if update was unsuccessful.
        """
        if key not in self.posts:
            return False
        
        post = self.posts.get(key)
        post.update_post(new_title, new_text)
        self.save_posts()
        return True


    def delete_post(self, key):
        """
        Delete a post from the given key.
        Return True if deletion was successful.
        Returns False if the post does not exists.
        """
        if key not in self.posts:
            return False

        self.posts.pop(key)
        self.save_posts()
        return True

    
    def list_posts(self):
        """
        List all Posts in order.
        Returns a list of sorted Posts.
        """

        return list(self.posts.values())[::-1]