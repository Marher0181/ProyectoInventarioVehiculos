USE [Inventario_Vehiculos]
GO

/****** Object:  Table [dbo].[Cliente]    Script Date: 05/09/2024 05:38:01 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Cliente](
	[idCliente] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](100) NULL,
	[dpi] [varchar](100) NULL,
	[correo] [varchar](100) NULL,
	[telefono] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[idCliente] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO



USE [Inventario_Vehiculos]
GO

/****** Object:  Table [dbo].[Vehiculo]    Script Date: 05/09/2024 05:37:19 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Vehiculo](
	[idVehiculo] [int] IDENTITY(1,1) NOT NULL,
	[marca] [varchar](100) NULL,
	[modelo] [varchar](100) NULL,
	[anio] [int] NULL,
	[precio] [decimal](10, 2) NULL,
	[disponibilidad] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[idVehiculo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Vehiculo] ADD  DEFAULT ((1)) FOR [disponibilidad]
GO


USE [Inventario_Vehiculos]
GO

/****** Object:  Table [dbo].[Venta]    Script Date: 05/09/2024 05:37:26 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Venta](
	[idVenta] [int] IDENTITY(1,1) NOT NULL,
	[idVehiculo] [int] NULL,
	[idCliente] [int] NULL,
	[fechaVenta] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[idVenta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Venta] ADD  DEFAULT (getdate()) FOR [fechaVenta]
GO

ALTER TABLE [dbo].[Venta]  WITH CHECK ADD  CONSTRAINT [fk_Cliente] FOREIGN KEY([idCliente])
REFERENCES [dbo].[Cliente] ([idCliente])
GO

ALTER TABLE [dbo].[Venta] CHECK CONSTRAINT [fk_Cliente]
GO

ALTER TABLE [dbo].[Venta]  WITH CHECK ADD  CONSTRAINT [fk_vehiculo] FOREIGN KEY([idVehiculo])
REFERENCES [dbo].[Vehiculo] ([idVehiculo])
GO

ALTER TABLE [dbo].[Venta] CHECK CONSTRAINT [fk_vehiculo]
GO

USE [Inventario_Vehiculos]
GO

CREATE PROCEDURE sp_RegistrarVenta
    @idVehiculo INT,
    @idCliente INT
AS
BEGIN
    BEGIN TRANSACTION;
    
    BEGIN TRY
        INSERT INTO Venta (idVehiculo, idCliente)
        VALUES (@idVehiculo, @idCliente);

        UPDATE Vehiculo
        SET disponibilidad = 0
        WHERE idVehiculo = @idVehiculo;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO
