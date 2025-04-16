import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../../services/api';
import { Message, Account } from '../../types';

interface MessagesState {
  messages: Message[];
  conversations: {
    [key: number]: Message[];
  };
  currentChat: {
    user: Account | null;
    messages: Message[];
  };
  loading: boolean;
  error: string | null;
}

const initialState: MessagesState = {
  messages: [],
  conversations: {},
  currentChat: {
    user: null,
    messages: [],
  },
  loading: false,
  error: null,
};

export const fetchInbox = createAsyncThunk('messages/fetchInbox', async () => {
  const response = await api.get<Message[]>('messages/inbox/');
  return response.data;
});

export const sendMessage = createAsyncThunk(
  'messages/sendMessage',
  async ({ receiverId, content }: { receiverId: number; content: string }) => {
    const response = await api.post<Message>('messages/send-message/', {
      message_receiver: receiverId,
      content,
    });
    return response.data;
  }
);

export const deleteMessage = createAsyncThunk(
  'messages/deleteMessage',
  async (messageId: number) => {
    await api.delete(`messages/delete/${messageId}/`);
    return messageId;
  }
);

const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    setCurrentChat: (state, action) => {
      state.currentChat.user = action.payload;
      state.currentChat.messages =
        state.conversations[action.payload.id] || [];
    },
    clearCurrentChat: (state) => {
      state.currentChat = {
        user: null,
        messages: [],
      };
    },
    addMessage: (state, action) => {
      const message = action.payload;
      const conversationId =
        message.message_sender.id === state.currentChat.user?.id
          ? message.message_sender.id
          : message.message_receiver.id;

      if (!state.conversations[conversationId]) {
        state.conversations[conversationId] = [];
      }
      state.conversations[conversationId].push(message);

      if (state.currentChat.user?.id === conversationId) {
        state.currentChat.messages.push(message);
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Inbox
      .addCase(fetchInbox.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInbox.fulfilled, (state, action) => {
        state.loading = false;
        state.messages = action.payload;
        
        // Organize messages by conversation
        state.conversations = action.payload.reduce((acc, message) => {
          const conversationId =
            message.message_sender.id === state.currentChat.user?.id
              ? message.message_sender.id
              : message.message_receiver.id;

          if (!acc[conversationId]) {
            acc[conversationId] = [];
          }
          acc[conversationId].push(message);
          return acc;
        }, {} as { [key: number]: Message[] });

        // Update current chat if exists
        if (state.currentChat.user) {
          state.currentChat.messages =
            state.conversations[state.currentChat.user.id] || [];
        }
      })
      .addCase(fetchInbox.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch messages';
      })
      // Send Message
      .addCase(sendMessage.fulfilled, (state, action) => {
        const message = action.payload;
        const conversationId = message.message_receiver.id;

        if (!state.conversations[conversationId]) {
          state.conversations[conversationId] = [];
        }
        state.conversations[conversationId].push(message);

        if (state.currentChat.user?.id === conversationId) {
          state.currentChat.messages.push(message);
        }
      })
      // Delete Message
      .addCase(deleteMessage.fulfilled, (state, action) => {
        const messageId = action.payload;
        state.messages = state.messages.filter((m) => m.id !== messageId);
        
        if (state.currentChat.user) {
          state.currentChat.messages = state.currentChat.messages.filter(
            (m) => m.id !== messageId
          );
          state.conversations[state.currentChat.user.id] =
            state.currentChat.messages;
        }
      });
  },
});

export const {
  setCurrentChat,
  clearCurrentChat,
  addMessage,
  clearError,
} = messagesSlice.actions;
export default messagesSlice.reducer; 