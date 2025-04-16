import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  TextField,
  IconButton,
  Avatar,
  Grid,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Favorite,
  FavoriteBorder,
  Comment as CommentIcon,
  Send as SendIcon,
} from '@mui/icons-material';
import { AppDispatch, RootState } from '../../store';
import { fetchPosts, createPost, likePost, addComment } from '../../store/slices/postsSlice';
import { Post } from '../../types';

const Home = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { posts, loading } = useSelector((state: RootState) => state.posts);
  const { account } = useSelector((state: RootState) => state.auth);
  
  const [newPostOpen, setNewPostOpen] = useState(false);
  const [newPostData, setNewPostData] = useState({
    title: '',
    descriptions: '',
    image: null as File | null,
  });
  const [commentText, setCommentText] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);

  const handleCreatePost = async () => {
    const formData = new FormData();
    formData.append('title', newPostData.title);
    formData.append('descriptions', newPostData.descriptions);
    if (newPostData.image) {
      formData.append('image', newPostData.image);
    }

    try {
      await dispatch(createPost(formData)).unwrap();
      setNewPostOpen(false);
      setNewPostData({ title: '', descriptions: '', image: null });
    } catch (error) {
      console.error('Failed to create post:', error);
    }
  };

  const handleLikePost = async (postId: number) => {
    try {
      await dispatch(likePost(postId)).unwrap();
    } catch (error) {
      console.error('Failed to like post:', error);
    }
  };

  const handleAddComment = async (postId: number) => {
    const content = commentText[postId];
    if (!content?.trim()) return;

    try {
      await dispatch(addComment({ postId, content })).unwrap();
      setCommentText({ ...commentText, [postId]: '' });
    } catch (error) {
      console.error('Failed to add comment:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <Container maxWidth="md">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography>Loading posts...</Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
              <Avatar
                src={account?.profile_image || undefined}
                alt={account?.user.username}
              />
              <Button
                variant="outlined"
                fullWidth
                onClick={() => setNewPostOpen(true)}
                sx={{ justifyContent: 'left', pl: 2 }}
              >
                What's on your mind?
              </Button>
            </Paper>
          </Grid>

          {posts.map((post: Post) => (
            <Grid item xs={12} key={post.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar
                      src={post.account.profile_image || undefined}
                      alt={post.account.user.username}
                      sx={{ mr: 2 }}
                    />
                    <Box>
                      <Typography variant="subtitle1">
                        {post.account.user.username}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {formatDate(post.created_at)}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="h6" gutterBottom>
                    {post.title}
                  </Typography>
                  <Typography variant="body1" paragraph>
                    {post.descriptions}
                  </Typography>
                </CardContent>
                {post.image && (
                  <CardMedia
                    component="img"
                    image={post.image}
                    alt={post.title}
                    sx={{ maxHeight: 500, objectFit: 'contain' }}
                  />
                )}
                <CardActions sx={{ px: 2, pb: 2 }}>
                  <IconButton
                    onClick={() => handleLikePost(post.id)}
                    color={post.likes.some(like => like.account === account?.id) ? 'primary' : 'default'}
                  >
                    {post.likes.some(like => like.account === account?.id) ? (
                      <Favorite />
                    ) : (
                      <FavoriteBorder />
                    )}
                  </IconButton>
                  <Typography variant="body2" color="text.secondary">
                    {post.likes.length} likes
                  </Typography>
                  <IconButton>
                    <CommentIcon />
                  </IconButton>
                  <Typography variant="body2" color="text.secondary">
                    {post.comments.length} comments
                  </Typography>
                </CardActions>
                <CardContent>
                  {post.comments.map((comment) => (
                    <Box
                      key={comment.id}
                      sx={{ display: 'flex', alignItems: 'start', mb: 2 }}
                    >
                      <Avatar
                        src={comment.account.profile_image || undefined}
                        alt={comment.account.user.username}
                        sx={{ width: 32, height: 32, mr: 1 }}
                      />
                      <Box
                        sx={{
                          backgroundColor: 'grey.100',
                          borderRadius: 2,
                          p: 1,
                          flex: 1,
                        }}
                      >
                        <Typography variant="subtitle2">
                          {comment.account.user.username}
                        </Typography>
                        <Typography variant="body2">{comment.content}</Typography>
                      </Box>
                    </Box>
                  ))}
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                    <TextField
                      fullWidth
                      size="small"
                      placeholder="Write a comment..."
                      value={commentText[post.id] || ''}
                      onChange={(e) =>
                        setCommentText({
                          ...commentText,
                          [post.id]: e.target.value,
                        })
                      }
                      onKeyPress={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          handleAddComment(post.id);
                        }
                      }}
                    />
                    <IconButton
                      onClick={() => handleAddComment(post.id)}
                      disabled={!commentText[post.id]?.trim()}
                    >
                      <SendIcon />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Dialog open={newPostOpen} onClose={() => setNewPostOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Post</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Title"
            fullWidth
            value={newPostData.title}
            onChange={(e) =>
              setNewPostData({ ...newPostData, title: e.target.value })
            }
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={4}
            value={newPostData.descriptions}
            onChange={(e) =>
              setNewPostData({ ...newPostData, descriptions: e.target.value })
            }
          />
          <input
            accept="image/*"
            type="file"
            onChange={(e) =>
              setNewPostData({
                ...newPostData,
                image: e.target.files ? e.target.files[0] : null,
              })
            }
            style={{ marginTop: 16 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewPostOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreatePost}
            disabled={!newPostData.title || !newPostData.descriptions}
          >
            Post
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Home; 