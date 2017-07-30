import sqlite3
def main():

    def create_post(conn, post):
        sql = ''' INSERT INTO posts(title,body,author,image_url,created_at)
                  VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, post)
        return cur.lastrowid

    def create_comment(conn, comment):
        sql = ''' INSERT INTO comments(content,author,post_id) VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, comment)
        return cur.lastrowid

    def create_user(conn, user):
        sql = ''' INSERT INTO users(username, password, created_at) VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, user)
        return cur.lastrowid

    database = "/Users/abbystarnes/Documents/Q3/reddit-clone-/reddit.db"

    conn = sqlite3.connect('reddit.db')
    with conn:
        # create a new post
        text1 = 'One Saturday morning at three'
        text2 = 'There was an Old Person of Chester'
        text3 = 'There was an Old Person of Rhodes'
        text4 = 'There was a young boy from Manassas'


        # posts
        post_1 = ('Cheesy Post', text1, 'Ironic Irma', 'https://images.pexels.com/photos/211050/pexels-photo-211050.jpeg?h=350&auto=compress', '12-17-2004')
        post_2 = ('Oldie but a Goodie', text2, 'Edward Lear', 'https://img.buzzfeed.com/buzzfeed-static/static/2015-11/19/10/enhanced/webdr13/anigif_enhanced-22345-1447947761-7.gif?downsize=715:*&output-format=auto&output-quality=auto', '11-11-2011')

        # create posts
        create_post(conn, post_1)
        create_post(conn, post_2)


        # comments
        comment_1 = ('Yikes!', 'Mom', 0)
        comment_2 = ('haha', 'Bob', 0)
        comment_3 = ('crazy', 'Hildegard', 2)

        # create comments
        create_comment(conn, comment_1)
        create_comment(conn, comment_2)
        create_comment(conn, comment_3)

        # users

        # create users

if __name__ == '__main__':
    main()
