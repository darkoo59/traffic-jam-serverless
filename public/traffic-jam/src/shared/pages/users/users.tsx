import * as React from "react";
import { UserCard } from '../../components/user-card';
import BannerBackground from "../images/banner-background.png";
import { User } from '../../models/user';
import { toast } from "react-toastify";
import { Container, Grid, Box, Backdrop, CircularProgress } from "@mui/material";
import { useCallback } from "react";
import { environment } from "../../../environments/environment";
import { BackendContext, BackendContextValue } from "../../contexts/backend-url-context";
import { useContext } from "react";

const Users = () => {
  const [users, setUsers] = React.useState<User[]>([]);
  const [loading, setLoading] = React.useState(true);
  const { url } = useContext<BackendContextValue>(BackendContext);

  const fetchUsers = useCallback(async () => {
    const response = await fetch(url+'/get-users');
    const data = await response.json();
    setUsers(data.users_data);
    setLoading(false);
  }, []);

  React.useEffect(() => {
      fetchUsers();
  }, []);
  return (
    <Container component="main" maxWidth="xs">
    <Box
      sx={{
        marginTop: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
    <div>
        <Grid container spacing={2}>
            {users.map((user) => (
              <React.Fragment key={user.email}>
                <Grid item xs={6} sm={4} md={5} lg={5} key={user.email}>
                <UserCard
                  user={user}
                  fetchUsers={fetchUsers}
                />
                </Grid>
              </React.Fragment>
            ))}
             </Grid>
    </div>
    </Box>
    <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </Container>
  );
            }

export default Users;