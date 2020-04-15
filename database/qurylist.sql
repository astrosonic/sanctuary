drop table roomlist

create table roomlist (RoomIdentity text primary key not null,
                       HashedPassword text not null,
                       RoomName text not null,
                       OwnerName text not null,
                       OperationStartTime text not null,
                       OperationStopTime text not null,
                       IsItPurged text not null,
                       PurgerName text not null,
                       TimeOfPurging text not null)

select * from roomlist;