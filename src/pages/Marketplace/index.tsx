import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  InputAdornment,
  Fab,
} from '@mui/material';
import { Add as AddIcon, Search as SearchIcon } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../../store';
import api from '../../services/api';
import { MarketProduct } from '../../types';

const Marketplace = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { account } = useSelector((state: RootState) => state.auth);
  
  const [products, setProducts] = useState<MarketProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [newProductOpen, setNewProductOpen] = useState(false);
  const [newProduct, setNewProduct] = useState({
    product_name: '',
    product_price: '',
    product_informations: '',
    product_image: null as File | null,
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get<MarketProduct[]>('market_products_list/');
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProduct = async () => {
    try {
      const formData = new FormData();
      formData.append('product_name', newProduct.product_name);
      formData.append('product_price', newProduct.product_price);
      formData.append('product_informations', newProduct.product_informations);
      if (newProduct.product_image) {
        formData.append('product_image', newProduct.product_image);
      }

      await api.post('add_product_market/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setNewProductOpen(false);
      setNewProduct({
        product_name: '',
        product_price: '',
        product_informations: '',
        product_image: null,
      });
      fetchProducts();
    } catch (error) {
      console.error('Failed to create product:', error);
    }
  };

  const filteredProducts = products.filter((product) =>
    product.product_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography>Loading marketplace...</Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
          <Typography variant="h4" component="h1">
            Marketplace
          </Typography>
          <TextField
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            size="small"
            sx={{ width: 300 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Box>

        <Grid container spacing={3}>
          {filteredProducts.map((product) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
              <Card>
                <CardMedia
                  component="img"
                  height="200"
                  image={product.product_image}
                  alt={product.product_name}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {product.product_name}
                  </Typography>
                  <Typography variant="h6" color="primary" gutterBottom>
                    ${product.product_price}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical',
                    }}
                  >
                    {product.product_informations}
                  </Typography>
                  <Box sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      Sold by {product.seller.user.username}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Fab
          color="primary"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => setNewProductOpen(true)}
        >
          <AddIcon />
        </Fab>

        <Dialog
          open={newProductOpen}
          onClose={() => setNewProductOpen(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>List New Product</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Product Name"
              fullWidth
              value={newProduct.product_name}
              onChange={(e) =>
                setNewProduct({ ...newProduct, product_name: e.target.value })
              }
            />
            <TextField
              margin="dense"
              label="Price"
              type="number"
              fullWidth
              value={newProduct.product_price}
              onChange={(e) =>
                setNewProduct({ ...newProduct, product_price: e.target.value })
              }
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">$</InputAdornment>
                ),
              }}
            />
            <TextField
              margin="dense"
              label="Description"
              fullWidth
              multiline
              rows={4}
              value={newProduct.product_informations}
              onChange={(e) =>
                setNewProduct({
                  ...newProduct,
                  product_informations: e.target.value,
                })
              }
            />
            <input
              accept="image/*"
              type="file"
              onChange={(e) =>
                setNewProduct({
                  ...newProduct,
                  product_image: e.target.files ? e.target.files[0] : null,
                })
              }
              style={{ marginTop: 16 }}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setNewProductOpen(false)}>Cancel</Button>
            <Button
              onClick={handleCreateProduct}
              disabled={
                !newProduct.product_name ||
                !newProduct.product_price ||
                !newProduct.product_informations ||
                !newProduct.product_image
              }
            >
              List Product
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default Marketplace; 