import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../services/api';
import { Post, Comment } from '../../types';

interface PostsState {
  posts: Post[];
  currentPost: Post | null;
  loading: boolean;
  error: string | null;
}

const initialState: PostsState = {
  posts: [],
  currentPost: null,
  loading: false,
  error: null,
};

export const fetchPosts = createAsyncThunk('posts/fetchPosts', async () => {
  const response = await api.get<Post[]>('post-list/');
  return response.data;
});

export const createPost = createAsyncThunk(
  'posts/createPost',
  async (formData: FormData) => {
    const response = await api.post<Post>('post/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
);

export const likePost = createAsyncThunk(
  'posts/likePost',
  async (postId: number) => {
    const response = await api.post('like/', { post: postId });
    return { postId, data: response.data };
  }
);

export const addComment = createAsyncThunk(
  'posts/addComment',
  async ({ postId, content }: { postId: number; content: string }) => {
    const response = await api.post<Comment>('add_comment/', {
      post: postId,
      content,
    });
    return response.data;
  }
);

const postsSlice = createSlice({
  name: 'posts',
  initialState,
  reducers: {
    setCurrentPost: (state, action: PayloadAction<Post>) => {
      state.currentPost = action.payload;
    },
    clearCurrentPost: (state) => {
      state.currentPost = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Posts
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch posts';
      })
      // Create Post
      .addCase(createPost.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createPost.fulfilled, (state, action) => {
        state.loading = false;
        state.posts.unshift(action.payload);
      })
      .addCase(createPost.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to create post';
      })
      // Like Post
      .addCase(likePost.fulfilled, (state, action) => {
        const post = state.posts.find((p) => p.id === action.payload.postId);
        if (post) {
          post.likes = action.payload.data.likes;
        }
        if (state.currentPost?.id === action.payload.postId) {
          state.currentPost.likes = action.payload.data.likes;
        }
      })
      // Add Comment
      .addCase(addComment.fulfilled, (state, action) => {
        const post = state.posts.find((p) => p.id === action.payload.post);
        if (post) {
          post.comments.push(action.payload);
        }
        if (state.currentPost?.id === action.payload.post) {
          state.currentPost.comments.push(action.payload);
        }
      });
  },
});

export const { setCurrentPost, clearCurrentPost, clearError } = postsSlice.actions;
export default postsSlice.reducer; 